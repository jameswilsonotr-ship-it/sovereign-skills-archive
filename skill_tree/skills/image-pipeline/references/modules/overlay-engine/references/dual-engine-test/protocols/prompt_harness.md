# Protocol — Dual-engine test harness entry
**Triggers:** `test`, `harness`, `test harness`, `dual engine test`, `run the harness` (with image context preferred).

## Steps
1. Load dual-engine-test coherence_map + this file.
2. Session isolation: new harness → menu all “Not run” for *this* session (history lives in registry only).
3. If no default six yet this session, run `prompt_default_six.md` first OR present menu and wait — prefer default six when image is present.
4. Present menu A–E, M2, M3 with status columns.
5. On letter reply, load the matching `prompt_option_*.md` or `prompt_m2_split.md` / `prompt_m3_merge.md`.
6. After each option: scores, run log row, re-present menu.
