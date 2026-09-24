#!/usr/bin/env python3
"""Call-site exercise for this engine against image-pipeline engine_hook."""
import json, subprocess, sys
from pathlib import Path

HOOK = Path("/home/workdir/.grok/skills/image-pipeline/scripts/engine_hook.py")
PY = sys.executable

CASES = [
    ("normal", "a portrait in soft light", True),
    ("random", "random pipeline", False),
    ("bunny1", "use bunny top 10 #1", False),
    ("named", "apply helmut newton graphic dominance", False),
    ("off", "pipeline off", True),
]

def run(text):
    out = subprocess.check_output([PY, str(HOOK), text], text=True)
    return json.loads(out)

def main():
    failed = 0
    for name, text, expect_pt in CASES:
        try:
            r = run(text)
        except Exception as e:
            print(f"FAIL {name}: hook error {e}")
            failed += 1
            continue
        pt = bool(r.get("pass_through"))
        err = r.get("error")
        if err:
            print(f"FAIL {name}: error={err}")
            failed += 1
            continue
        if pt != expect_pt:
            print(f"FAIL {name}: pass_through={pt} expected {expect_pt}")
            failed += 1
            continue
        if not pt and not r.get("prompt_terms"):
            print(f"FAIL {name}: expected prompt_terms")
            failed += 1
            continue
        print(f"PASS {name}: mode={r.get('pipeline_mode')} terms={len(r.get('prompt_terms') or [])}")
    print("---")
    if failed:
        print(f"FAILED {failed} case(s)")
        sys.exit(1)
    print("ENGINE CALL-SITE HARNESS PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()
