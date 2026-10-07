#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime as dt
import json
import platform
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "infrastructure/system-manifest.json"
HISTORY = ROOT / "infrastructure/history/infrastructure-history.jsonl"

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
    out = run(["dpkg-query", "-W", "-f=%{Package}\t%{Version}\n"], 60)
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
        "schema_version": "1.0",
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

def append(events, timestamp):
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as f:
        for action, manager, package, old, new in events:
            record = {
                "schema_version": "1.0",
                "timestamp": timestamp,
                "actor": "unknown",
                "source": "reconciliation",
                "confidence": "detected",
                "action": action,
                "manager": manager,
                "package": package,
                "from": old,
                "to": new,
                "reason": None,
                "status": "observed"
            }
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-git", action="store_true")
    args = ap.parse_args()

    old = load(MANIFEST, {})
    new = observe()
    first = not bool(old.get("packages"))
    events = [] if first else changes(old, new)
    save(MANIFEST, new)

    if first:
        append([["baseline", "system", "", "", "initial_observation"]], new["generated_at"])
    elif events:
        append(events, new["generated_at"])

    if not args.no_git and (first or events) and exists("git"):
        subprocess.run(["git", "add", str(MANIFEST), str(HISTORY)], cwd=ROOT, check=False)
        subprocess.run(["git", "commit", "-m", "infra: reconcile infrastructure state"],
                       cwd=ROOT, check=False)

    if not args.quiet:
        print(json.dumps({"first_run": first, "events": len(events),
                          "manifest": str(MANIFEST), "history": str(HISTORY)},
                         ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
