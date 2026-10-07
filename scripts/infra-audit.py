#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"infrastructure/system-manifest.json"
DESIRED=ROOT/"infrastructure/desired-state.json"
HISTORY=ROOT/"infrastructure/history/infrastructure-history.jsonl"

def load(p, default):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError): return default

def main():
    ap=argparse.ArgumentParser(description="Audita infraestructura observada contra intención declarada.")
    ap.add_argument("--json", action="store_true")
    args=ap.parse_args()

    manifest=load(MANIFEST,{})
    desired=load(DESIRED,{})
    packages=manifest.get("packages",{})
    wanted=desired.get("package_managers",{})
    findings=[]

    for manager, state in packages.items():
        groups=wanted.get(manager,{})
        required=set(groups.get("required",[]))
        optional=set(groups.get("optional",[]))
        temporary=set(groups.get("temporary",[]))
        for package, version in state.items():
            if package in temporary:
                classification="temporary"
                action="review"
            elif package in required:
                classification="required"
                action="keep"
            elif package in optional:
                classification="optional"
                action="review"
            else:
                classification="unmanaged"
                action="review"
            findings.append({
                "manager":manager,"package":package,"version":version,
                "classification":classification,"action":action
            })

    summary={}
    for f in findings:
        summary[f["classification"]]=summary.get(f["classification"],0)+1

    result={
        "schema_version":"1.0",
        "purpose":"Evidence-based infrastructure audit; never an automatic removal plan.",
        "summary":summary,
        "findings":findings
    }
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else
          "\n".join(f'{x["manager"]}: {x["package"]} {x["version"]} -> {x["classification"]} ({x["action"]})'
                    for x in findings))
if __name__=="__main__":
    main()
