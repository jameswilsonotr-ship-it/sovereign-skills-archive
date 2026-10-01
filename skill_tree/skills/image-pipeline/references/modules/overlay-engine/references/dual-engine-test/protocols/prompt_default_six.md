# Protocol — Default six (parameterized)

**Engine:** generate = pure text-to-image / plate-anchored; overlay = edit/reference path.  
**Planner SSOT:** `scripts/default_six.py` (Section 4 — 2026-07-29)

## Modes

| Mode | When | Slots 1–4 | Slots 5–6 |
|------|------|-----------|-----------|
| **classic_dual** | `characters` empty or `[olivia, bunny]` | Liv/Bunny presentable + tight | **M2 / M3** Liv+Bunny merge engines |
| **single_entity** | one resolved entity (e.g. `shauna`) | Presentable overlay + plate-anchored; tight overlay + plate-anchored | **M2/M3 experimental** hybrid vs source (not Liv+Bunny merge) |
| **multi_entity** | two or more non-classic sets | Presentable + tight per primary character | Classic M2/M3 only if both Liv+Bunny present; else experimental |

## IP-WQ-038 — Tool phase first (mandatory)

**No final image response without tool receipts.**

Before step 3 (Emit):
1. Execute generate/edit/render tool calls for every planned slot.
2. Collect artifact IDs for this turn.
3. Echo gate: `planned_slots` vs `len(artifact_ids)`. If short → BLOCK emit, retry tools.
4. Only then emit titles + images + prompt blocks.
5. FORENSICS must include `emit_without_generate: pass|fail` (fail = protocol violation).

Skipping the tool phase and writing render tags anyway is the exact failure this rule exists to prevent.

## Steps

1. Load `prompt_display_rules.md` + `prompt_scoring.md` + `modules/shared/scoring_and_forensics.md`.
2. Build plan: `python scripts/default_six.py --brief '<BRIEF>'` (optional `--with-intent`).
3. Emit **six images in plan order** using each slot’s `label`, `character`, `branch_pref`, `anchor` / `preferred_plate`.
4. Each: bold title → image (short alt) → one prompt code block → **score line (mandatory)**.
5. If entity has hair lock (Shauna V7): add **`hair_texture: pass | fail | soft`** on the score line.
6. **SET SCORES** summary (mandatory — even if renders were staged earlier and fired this turn).
7. **FORENSICS** panel (mandatory): `echo_dna_*`, `mira.*`, anchors, `dna_fallback`, `hair_texture_gate`, packs.
8. Present menu (A–E, M2, M3, Packs) with statuses for **this session only**.
9. Optional: descriptive rename via `rename_artifacts.py` if files exist on disk.

**Incomplete without steps 4–7.** Staged “READY” without later scores/forensics is a protocol fail.

## Agent policy (locked entities)

- Prefer **edit-from preferred canonical plate** over blank pure generate when `preferred_plate` is set.
- On **0-byte** write: retry that slot once sequentially, then failover.
- **True M2/M3 merge engines stay Liv+Bunny-only.** `M2_experimental` / `M3_experimental` are hybrid-vs-source only.

## Do not

- Invent M1 or F.
- Inject old session averages into a fresh menu as “already run”.
- Run Liv+Bunny merge labels when the plan mode is `single_entity` for Shauna (or any non-dual).
