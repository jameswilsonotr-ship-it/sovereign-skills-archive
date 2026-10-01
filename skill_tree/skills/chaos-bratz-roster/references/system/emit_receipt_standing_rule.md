# Standing Rule — Visual Emit Requires Receipts

**Status**: ACTIVE 2026-08-13  
**Source**: IP-WQ-038 / IP-WQ-039 / CBR-WQ-001

```
No image-bearing final response may claim picture slots unless matching
tool receipts cover planned_slots for this turn.
```

If short → BLOCK. Retry tools. Never invent pictures.

Helper: `image-pipeline/scripts/emit_gate.py`  
Forensics: `emit_without_generate: pass|fail` (fail = protocol violation)

Applies to every roster agent and every orchestrator path that can request images.
