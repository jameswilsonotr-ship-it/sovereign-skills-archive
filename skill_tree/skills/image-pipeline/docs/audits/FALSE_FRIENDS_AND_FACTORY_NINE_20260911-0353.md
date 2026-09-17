# False friends explained + factory nine

stamp: 2026-09-11 03:53 EDT

## Why “false friends” was parked

Parked did **not** mean “ignore forever.” It meant: do not run the same resurrection pass we ran on CBR/claim, because those words inside image-pipeline are almost never **skill dependencies**.

Recount on IP `{md,py,json,yaml}` tonight:

| word | `/skills/<slug>` path hits | name hits | what the name hits actually are |
|---|---|---|---|
| valerie | 1 — and that 1 is **our own audit markdown** saying “not a path” | 34 | Valerie the agent / Risk Officer / visual DNA. There *is* a `/skills/valerie` skill. IP does not call its scripts. |
| color | 0 | 34 | hair color, CSS, wardrobe. `/skills/color` is not even on disk tonight. |
| tasks | 0 | 5 | overlay “tasks” prose. `/skills/tasks` not on disk tonight. |
| pdf | 0 | 3 | “PDF” as a file type in overlay notes. Bundled pdf skill exists under `/root/.grok/skills/pdf`. IP emit does not call it. |
| mcp | 0 | 1 | connectors/add-connector.md |

So: a skill *can* exist (valerie, pdf) and still not be an IP wiring target. Hunting their missing files would be a different job, not “IP is broken because it said Valerie.” That is why D waited behind the factory nine that SKILL.md actually lists as scripts.

Unpark anytime. Next D pass would be: audit `/skills/valerie` on its own completeness, not because IP points at it.

## Factory nine

Drive exact-name: `split_plan.py`, `inbound_classify.py`, `emit_intent.py`, `isolate_person.py` — **zero files**.

Local: only `engine_hook.py` shims under generate-engine / overlay-engine, pointing at a missing `image-pipeline/scripts/engine_hook.py`.

Reconstructed tonight from `references/modules/split-engine/PROTOCOL.md` CLI + isolate section. Marked reconstructed. Smoke `--help` on all siblings + keep_path: ok.

Not SAM. Classify is filename + aspect-ratio heuristic. Segment is equal PIL crops.
