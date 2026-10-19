# IPQ-078 — Keep path

**Status:** LIVE scripts on disk 2026-09-11. Protocol file restored this turn (was a completeness gap).
**Scripts:** `scripts/keep_path.py` · `scripts/step6_drive_flush.py` · `scripts/flush_drive_queue.py`
**Claim:** Absolute Liv HUB

## Contract

Session receipt → triple:

- jpeg
- sibling `.prompt.md` (same basename, not optional)
- `.keep.json`

Local A: `/home/workdir/artifacts/rendered/`
Local B: `references/visuals/keeps/YYYY/MM/`
Drive: Liv-HUB image-pipeline-keeps (agent flush)

`--slug` wins. Else auto-slug from agent + prompt tokens.

```
python scripts/keep_path.py --src receipt.jpg --auto-slug --agent olivia --prompt "exact tool prompt"
```

## Step 6

`step6_drive_flush.py --plan` then `--gate`.
`--gate` exit 0 = flushed. Exit 2 = talking while unflushed is a protocol fail.

`flush_drive_queue.py --mark --inventory` after upload.

## Tested 2026-09-11

- keep_path / step6 / flush present and compile
- factory smoke `--help` includes keep_path
- full JPEG lake flush not re-run this turn (already gated earlier in the 170 restore)

## Blocked

Host skill-tree churn can delete these files. Durable copy: Drive `05_SOURCE_PACKS` + `06_CROSS_SKILL_AUDIT`.
