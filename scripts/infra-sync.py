#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime as dt
import json
import platform
import re
import shlex
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "infrastructure/system-manifest.json"
HISTORY = ROOT / "infrastructure/history/infrastructure-history.jsonl"
OP_LOG = Path.home() / ".infra-package-operations.jsonl"
OP_CURSOR = ROOT / "infrastructure/history/package-operation-cursor.json"
LEGACY_PKG_LOG = Path.home() / ".infra-pkg-operations.log"
LEGACY_PKG_CURSOR = ROOT / "infrastructure/history/pkg-operation-cursor.json"
NOTES_LOG = Path.home() / ".infra-notes.jsonl"

def run(cmd, timeout=30):
    try:
        p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL, timeout=timeout, check=False)
        return p.stdout.strip() if p.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""

def exists(name):
    return shutil.which(name) is not None

def version(cmd):
    out = run(cmd)
    return out.splitlines()[0].strip()[:200] if out else None

def load(path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")

def pkg_state():
    if not exists("dpkg-query"):
        return {}
    out = run(["dpkg-query", "-W", "-f=${Package}\t${Version}\n"], 60)
    result = {}
    for line in out.splitlines():
        if "\t" in line:
            name, ver = line.split("\t", 1)
            if name and ver:
                result[name] = ver
    return dict(sorted(result.items()))

def pip_state():
    py = shutil.which("python") or shutil.which("python3")
    if not py:
        return {}
    try:
        rows = json.loads(run([py, "-m", "pip", "list", "--format=json"], 60))
    except json.JSONDecodeError:
        return {}
    return dict(sorted((x["name"].lower(), x["version"]) for x in rows
                       if isinstance(x, dict) and x.get("name") and x.get("version")))

def npm_state():
    if not exists("npm"):
        return {}
    try:
        data = json.loads(run(["npm", "list", "-g", "--depth=0", "--json"], 60))
    except json.JSONDecodeError:
        return {}
    deps = data.get("dependencies", {}) if isinstance(data, dict) else {}
    return dict(sorted((name, meta["version"]) for name, meta in deps.items()
                       if isinstance(meta, dict) and meta.get("version")))

def gem_state():
    if not exists("gem"):
        return {}
    result = {}
    for line in run(["gem", "list", "--local"], 60).splitlines():
        m = re.match(r"^([^ (]+) \(([^)]+)\)$", line.strip())
        if m:
            result[m.group(1)] = m.group(2)
    return dict(sorted(result.items()))

def ssh_hosts():
    path = Path.home() / ".ssh/config"
    if not path.exists():
        return []
    hosts = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^\s*Host\s+(.+)$", line)
        if m:
            hosts += [x for x in m.group(1).split() if "*" not in x and "?" not in x]
    return sorted(set(hosts))

def observe():
    py = shutil.which("python") or shutil.which("python3")
    return {
        "schema_version": "1.1",
        "generated_by": "scripts/infra-sync.py",
        "purpose": "Observed current state of the Termux environment.",
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "system": {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "architecture": platform.machine(),
            "python_implementation": platform.python_implementation(),
            "termux_info": version(["termux-info"]) if exists("termux-info") else None
        },
        "runtimes": {
            "python": version([py, "--version"]) if py else None,
            "node": version(["node", "--version"]) if exists("node") else None,
            "npm": version(["npm", "--version"]) if exists("npm") else None,
            "git": version(["git", "--version"]) if exists("git") else None,
            "zsh": version(["zsh", "--version"]) if exists("zsh") else None
        },
        "package_managers": {
            "pkg": exists("pkg"),
            "pip": bool(py and run([py, "-m", "pip", "--version"])),
            "npm": exists("npm"),
            "gem": exists("gem")
        },
        "packages": {
            "pkg": pkg_state(),
            "pip": pip_state(),
            "npm_global": npm_state(),
            "gem": gem_state()
        },
        "configuration": {"ssh_host_profiles": ssh_hosts()}
    }

def changes(old, new):
    events = []
    for manager in sorted(new["packages"]):
        before = old.get("packages", {}).get(manager, {})
        after = new["packages"][manager]
        for name in sorted(set(before) | set(after)):
            if name not in before:
                events.append(["install", manager, name, "", after[name]])
            elif name not in after:
                events.append(["remove", manager, name, before[name], ""])
            elif before[name] != after[name]:
                events.append(["upgrade_or_downgrade", manager, name, before[name], after[name]])
    return events

def load_operations():
    operations = []
    if OP_LOG.exists():
        cursor = load(OP_CURSOR, {"processed_lines": 0})
        start = int(cursor.get("processed_lines", 0) or 0)
        try:
            lines = OP_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            lines = []
        for n, line in enumerate(lines, 1):
            if n <= start:
                continue
            try:
                item = json.loads(line)
                if isinstance(item, dict) and item.get("manager") and item.get("action"):
                    item["line"] = n
                    operations.append(item)
            except json.JSONDecodeError:
                continue
        return operations

    # Compatibilidad con el registro pkg de la versión anterior.
    if LEGACY_PKG_LOG.exists():
        cursor = load(LEGACY_PKG_CURSOR, {"processed_lines": 0})
        start = int(cursor.get("processed_lines", 0) or 0)
        try:
            lines = LEGACY_PKG_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            lines = []
        for n, line in enumerate(lines, 1):
            if n <= start:
                continue
            parts = line.split("\t", 2)
            if len(parts) == 3:
                occurred_at, action, command = parts
                operations.append({
                    "line": n,
                    "occurred_at": occurred_at.strip() or None,
                    "manager": "pkg",
                    "action": action.strip(),
                    "command": command.strip()
                })
    return operations

def load_notes():
    if not NOTES_LOG.exists():
        return []
    try:
        lines = NOTES_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []
    result = []
    for line in lines:
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                result.append(item)
        except json.JSONDecodeError:
            pass
    return result

def operation_package_names(operation):
    try:
        args = shlex.split(operation.get("command", ""))
    except ValueError:
        args = operation.get("command", "").split()
    if not args:
        return set()
    action = operation.get("action")
    skip = {"-y", "--yes", "-q", "--quiet", "-v", "--verbose", "--no-cache",
            "-g", "--global", "--local", "--user", "--upgrade", "-U"}
    names = set()
    for token in args[1:]:
        if token in skip or token.startswith("-"):
            continue
        if "=" in token and token.startswith("--"):
            continue
        names.add(token.strip())
    if action in {"upgrade", "update", "full-upgrade", "dist-upgrade"} and not names:
        return set()
    return names

def operation_matches(event, operation):
    if event[1] != operation.get("manager"):
        return False
    action = event[0]
    op = operation.get("action")
    if op == "update":
        return False
    allowed = {
        "install": {"install", "reinstall"},
        "remove": {"remove", "uninstall"},
        "upgrade_or_downgrade": {"upgrade", "update", "full-upgrade", "dist-upgrade", "reinstall"},
        "reinstall": {"reinstall"}
    }
    if op not in allowed.get(action, set()):
        return False
    names = operation_package_names(operation)
    if names:
        return event[2] in names
    return action == "upgrade_or_downgrade"

def parse_time(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value)
    except ValueError:
        return None

def find_note(manager, package, detected_at):
    target = parse_time(detected_at)
    if target is None:
        return None
    best = None
    for note in load_notes():
        if note.get("manager") != manager or note.get("package") != package:
            continue
        t = parse_time(note.get("timestamp"))
        if t is None:
            continue
        delta = abs((target - t).total_seconds())
        if delta <= 1800 and (best is None or t > parse_time(best["timestamp"])):
            best = note
    return best

def operation_events(operations, state_events):
    events = []
    represented = {
        (event[1], event[2])
        for event in state_events
    }

    for op in operations:
        action = op.get("action")
        manager = op.get("manager")

        # update solo actualiza índices/repositorios; no representa
        # por sí mismo un cambio de paquete.
        if action == "update":
            continue

        names = operation_package_names(op)

        # Operaciones explícitas que pueden existir aunque el estado final
        # sea idéntico, especialmente reinstall.
        if action == "reinstall":
            for package in sorted(names):
                key = (manager, package)
                if key in represented:
                    continue
                events.append([
                    "reinstall",
                    manager,
                    package,
                    None,
                    None
                ])

    return events


def append(events, detected_at, operations):
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as f:
        for event in events:
            action, manager, package, old, new = event
            occurred_at = None
            occurred_at_source = None
            evidence_command = "state observation"
            evidence_method = "state_comparison"

            matches = [op for op in operations if operation_matches(event, op)]
            if matches:
                op = matches[0]
                occurred_at = op.get("occurred_at")
                occurred_at_source = f'{op.get("manager")}_wrapper'
                evidence_command = op.get("command", evidence_command)
                evidence_method = "state_comparison+operation_log"

            note = find_note(manager, package, occurred_at or detected_at)
            record = {
                "schema_version": "1.2",
                "detected_at": detected_at,
                "occurred_at": occurred_at,
                "occurred_at_source": occurred_at_source,
                "actor": note.get("actor", "unknown") if note else "unknown",
                "actor_source": "infra_note" if note else None,
                "source": "reconciliation",
                "confidence": "declared+detected" if note else "detected",
                "action": action,
                "manager": manager,
                "package": package,
                "from": old,
                "to": new,
                "reason": note.get("reason") if note else None,
                "reason_source": "infra_note" if note else None,
                "evidence": {
                    "method": evidence_method,
                    "command": evidence_command
                },
                "status": "observed"
            }
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-git", action="store_true")
    ap.add_argument("--git-commit", action="store_true")
    args = ap.parse_args()

    old = load(MANIFEST, {})
    new = observe()
    first = old.get("generated_at") is None
    events = [] if first else changes(old, new)
    operations = load_operations()
    save(MANIFEST, new)

    if first:
        append([["baseline", "system", "", "", "initial_observation"]], new["generated_at"], [])
    else:
        events.extend(operation_events(operations, events))
        if events:
            append(events, new["generated_at"], operations)

    if operations and OP_LOG.exists():
        save(OP_CURSOR, {"schema_version": "1.0", "processed_lines": operations[-1]["line"]})

    if not args.no_git and args.git_commit and (first or events) and exists("git"):
        subprocess.run(["git", "add", str(MANIFEST), str(HISTORY), str(OP_CURSOR)],
                       cwd=ROOT, check=False)
        subprocess.run(["git", "commit", "-m", "infra: reconcile infrastructure state"],
                       cwd=ROOT, check=False)

    if not args.quiet:
        print(json.dumps({
            "first_run": first,
            "events": len(events),
            "operations_correlated": len(operations),
            "manifest": str(MANIFEST),
            "history": str(HISTORY)
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
