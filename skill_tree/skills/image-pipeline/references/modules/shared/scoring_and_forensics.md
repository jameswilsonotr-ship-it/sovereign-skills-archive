# Scoring + Forensics (IPQ-019 + IPQ-022)

**Status**: LIVE 2026-07-25  
**Applies to**: generate-engine, overlay-engine, render_engine path, default-six, options A–E, harness

---

## IPQ-019 — Mandatory scoring

**No image reply is complete without score lines.**

### Per image (required)
```
score: DNA _/10 | Pose _/10 | Outfit _/10 | Overall _/10 | note: <short>
tingly: yes | no | meh
```

### After default-six or any multi-image batch (required)
```
SET SCORES
1  Liv Presentable     Overall x.x
2  Bunny Presentable   Overall x.x
3  Liv Tight           Overall x.x
4  Bunny Tight         Overall x.x
5  Split M2            Overall x.x
6  Full merge M3       Overall x.x
avg overall: x.x
```

If renders were staged then fired later, scores still must appear **immediately after the images**, not only in a later turn.

Source of truth also lives in:
`modules/generate-engine/references/dual-engine-test/protocols/prompt_scoring.md`

---

## IPQ-022 — Forensics panel

### Default
- **Harness / field-test / default-six / option A–E**: ON
- **Quiet normal mode**: OFF unless `review on` / `with forensics`

### Toggle
| Phrase | Effect |
|--------|--------|
| `forensics on` / `with forensics` | Force ON for this turn + batch |
| `forensics off` / `no forensics` | Suppress panel |
| `review on` | Implies forensics ON |

### Panel format (when ON) — emit after scores
```
FORENSICS
echo_dna_injected: [A, B] | [] 
echo_dna_flag: INJECTED:A,B | NONE | CONFLICT
mira.drift_score: 0.0..1.0
mira_approved: true|false
mira.flags: [...]
height_lock: applied | n/a
packs: [...] | none
implication: [...] | none
moderation_scaleback: none | artistic | artistic+implication
emit_without_generate: pass | fail
```

`emit_without_generate` (IP-WQ-038): **pass** only if tool receipts (artifact IDs) covered planned slots before emit. **fail** is a hard protocol violation for the turn regardless of visual scores.

If Echo/Mira were not run (should not happen under IPQ-020), panel must say:
`FORENSICS: gate_skipped — Echo compose required`

---

## Order in every image-bearing reply

1. Title(s) + image(s) + prompt code block(s)  
2. **score** line(s) per image  
3. **SET SCORES** if batch  
4. **FORENSICS** if on  
5. Menu / next actions  

Skipping 2–3 is a protocol violation.
