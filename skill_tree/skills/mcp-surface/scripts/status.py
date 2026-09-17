#!/usr/bin/env python3
"""mcp-surface status — unified view of modules and fold state."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "references" / "modules"
STATE = ROOT / "state" / "state.json"
EXPECTED = ["bootstrap", "auditor", "sovereign-bridge", "catalog-browser"]

def main():
    print("mcp-surface status")
    print("=" * 40)
    if STATE.exists():
        try:
            data = json.loads(STATE.read_text())
            print(f"version:  {data.get('version', '?')}")
            print(f"status:   {data.get('status', '?')}")
            print(f"date:     {data.get('date', '?')}")
        except Exception as e:
            print(f"state:    (unreadable: {e})")
    else:
        print("state:    (missing)")
    print()
    print("modules:")
    for name in EXPECTED:
        path = MODULES / name
        skill = path / "SKILL.md"
        if skill.exists():
            print(f"  [ok]  {name}")
        elif path.is_dir():
            print(f"  [..]  {name} (dir only, no SKILL.md)")
        else:
            print(f"  [!!]  {name} MISSING")
    print()
    print("primary interface: mcp-surface")
    print("old top-level MCP skills: deleted (folded here)")

if __name__ == "__main__":
    main()
