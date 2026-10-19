#!/usr/bin/env python3
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "references" / "modules"
EXPECTED = ["miner","biomimetic","multi-variation","liv-bunny","iron-pearl","blackwell","heavy-dev"]
print("swarm-surface status")
print("="*40)
if (ROOT/"state"/"state.json").exists():
    print(json.loads((ROOT/"state"/"state.json").read_text()))
print("modules:")
for n in EXPECTED:
    ok = (MOD/n/"SKILL.md").exists() or (MOD/n/"README.md").exists()
    print(f"  [{'ok' if ok else '!!'}]  {n}")
