# FBQ-015 — emit_envelope helper: YAML + thin dash from one JSON

**Status**: OPEN  
**Parent**: SR-WQ-072  
**Home**: format-bible

Add `scripts/engine.py --emit` (or `emit_envelope.py`) that prints:
1. fenced yaml (skill/mode/time/date/summary/tags/debug_outcome)
2. `---`
3. `format_dashboard_thin()`

Model copies. Does not invent Ache. Heat stays off YAML.
