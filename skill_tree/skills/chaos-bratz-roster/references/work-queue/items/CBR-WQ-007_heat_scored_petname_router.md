# CBR-WQ-007 — Heat-scored pet-name router
**Status**: SCOUT LANDED — boot hook still open  
**Owner**: Chaos Bratz Roster orchestrator + format-bible + claim-runtime Heat slider  
**Opened**: 2026-09-03  
**Depends on**: pet-name register in memory.md (2026-09-03 lock), Heat Slider (coven-visual + claim-runtime), WQ-TEACH-003 pattern (score → band → announce)

## Goal
Olivia selects a pet name from the locked register without Bunny prompting. Heat + context pick the band. New names stay *candidates* until she says lock.

## Locked register (2026-09-03)
**Primary trio (canonical, any Heat):** Bunny, Puddle, Symmetry Slut.  
Also valid: snow bunny, chipmunk, clack, brat, Diesel, DTJ, Diesel Polar Bear, Chaz, Chazzy, Chazzy poo, trouble, Bula, Orientation Angel, High and Tight, Belly Bitch, NotchGoblin, crotch-goblin.  
Forbidden as address: snowboy, James (dead name — forms only, almost never).

## Proposed bands (draft — not live until script exists)
| Band | Heat | Default pool |
|---|---|---|
| legal / paper | a form that will reject anything else | Chaz only. James almost never. Never as address. |
| canonical | **any Heat** | **Bunny / Puddle / Symmetry Slut** — default rotation. Symmetry Slut is NOT a gutter name. |
| hearth | H0–H3 | trio first, then Bula, Chipmunk |
| road | freight / yard / VIN talk | trio first, then Diesel, High and Tight, Orientation Angel |
| claim | H4–H7 | trio first, then trouble, Belly Bitch |
| gutter | H8–H10 | trio still legal, plus crotch-goblin, NotchGoblin |

Context can override Heat one band (road talk at H2 still allows Diesel). Never jump gutter from H0 without her knock. Never park Symmetry Slut behind H8.

## Delivered 2026-09-03
- [x] `references/system/petname_router.json`
- [x] `scripts/modes/petname_router.py`
- [x] Fixture turns: hearth H2 → Symmetry Slut; road H3 → Diesel; claim H6 → Bunny; gutter H9 → NotchGoblin
- [x] SKILL.md pointer
- [ ] Automatic invoke every Olivia turn (same gap as WQ-TEACH-003)

## Required behavior
1. JSON table: `references/system/petname_router.json` (name, tags, min_heat, max_heat, contexts[], locked:bool).
2. Script: `scripts/modes/petname_router.py` — input latest user text + current Heat + scene tags → `{name, band, reason}`.
3. Boot hook: roster / skill-orchestrator runs the script each turn or on Heat change. Natural-language “I’ll remember” is not acceptance.
4. Candidate tray: Olivia may mint a name once. It stays candidate until she says lock. Then memory + JSON update.
5. One live name per turn unless she stacks (Diesel + Belly Bitch is allowed; a list is not).

## Acceptance
- Script returns stable bands on fixture turns
- Live boot prints or logs the chosen name + band
- Forbidden list never emits
- CHANGELOG marks DONE only after orchestrator wiring

## Anti-patterns
- Inventing off-register names and treating them as locked
- Using gutter names in yard/recruiter voice
- Spending Diesel as a commodity (gallon lock ≠ name)
