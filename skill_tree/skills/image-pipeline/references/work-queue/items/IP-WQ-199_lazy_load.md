# IP-WQ-199 — lazy-load refactor (PLAN ONLY)

**Status:** OPEN — do not implement this ticket
**Owner:** image-pipeline / skill-orchestrator
**Created:** 2026-09-11

SKILL.md is a full paste. Agentify, inbound feeds, keep-path, overlay, generate-engine all load when any visual trigger fires. 193 churn makes a fat tree expensive to reseat.

Suggested shape (not built):

1. Keep SKILL.md as a verb index + pointer table. No engine prose in the frontmatter block.
2. Load `references/modules/<engine>/SKILL.md` only when the verb hits that engine.
3. Inbound feeds (`fb_ingest` …) stay behind `feed_fork.py`. Do not import vendor until a URL is classified.
4. `scripts/vendor/` stays off `sys.path` until an ingest script runs.
5. Help / quickstart stay thin files, not inlined into SKILL.md.

Do not cut the tree apart in the same turn as a flush. This ticket is the plan.
