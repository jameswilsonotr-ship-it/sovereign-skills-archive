# ODA-WQ-043 — session_boot stays thin; optional prelude

**Status**: OPEN  
**Parent**: SR-WQ-072  
**Home**: olivia-dev-alpha

`scripts/session_boot.py` only runs wq_hygiene. Keep it that way. Optional flag `--prelude` may call roster `turn_prelude.py`. Never load expert triad or mirrors from session_boot.
