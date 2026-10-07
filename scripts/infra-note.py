#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json
from pathlib import Path

LOG = Path.home() / ".infra-notes.jsonl"

def main():
    ap = argparse.ArgumentParser(description="Registra intención humana para infraestructura.")
    ap.add_argument("manager")
    ap.add_argument("package")
    ap.add_argument("reason")
    ap.add_argument("--actor", default="user")
    ap.add_argument("--scope", default="temporary",
                    choices=["required","optional","temporary","investigation","unknown"])
    args = ap.parse_args()

    record = {
        "schema_version":"1.0",
        "timestamp":dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "manager":args.manager,
        "package":args.package,
        "reason":args.reason,
        "actor":args.actor,
        "scope":args.scope
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
