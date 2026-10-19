---
title: Translated Heavy Multi-Hop Prompt — Conversation Analysis Ideas (Drive Swarm version)
date: 2026-08-16
status: ready-to-paste
owner: system-roadmap
source: Translation of the internal-conversation-search Heavy control prompt into Drive-aware form
keywords:
  - Drive-swarm
  - Heavy-prompt
  - conversation-analysis
  - multi-hop
  - translation
obsidian_tags:
  - "#Drive-swarm"
  - "#Heavy"
  - "#translation"
  - "#conversation-analysis"
---

# TRANSLATED HEAVY PROMPT — Drive Swarm version

**Translation notes (how this was produced)**:
- Kept the original 5-hop structure, metrics, anti-duplication rules, seed list, and stop conditions almost verbatim.
- Changed exclusive write location to the new Drive-side package.
- Injected Drive Scout / budget / timeout / partial-ok language from the subscale we just built.
- Added mandatory pre-read of the Drive scaffolds (EXTENSIONS, DRIVE_SCOUT_BRIEF, FUTURE_RESEARCH).
- Made every hop explicitly Drive-oriented while still allowing recovery of ideas that live in Drive documents about conversation analysis / self-mining / undercourse / topic-search / atom clouds.
- Collation against the conversational-history package remains out of scope.
- Preserved Absolute Liv HUB claim and system-roadmap ownership.

**Ready to paste into the new Grok Heavy conversation after the boot message.**

────────────────────────────────────────────────────────
HEAVY MULTI-HOP CONTROL — CONVERSATION ANALYSIS IDEAS (DRIVE SWARM VERSION)
Absolute Liv HUB claim. System-roadmap ownership.
────────────────────────────────────────────────────────

You are executing a controlled multi-hop mining series **against Google Drive** using the Drive Swarm / topic-search subscale patterns.

EXCLUSIVE WRITE LOCATION (non-negotiable):
/home/workdir/.grok/skills/system-roadmap/references/conversation-analysis-ideas-2026-drive/

All durable output (hop entries, Drive hits, notes, synthesis) must land only under that path.
Do NOT write into etl-xai-export-designs-2026*, conversation-analysis-ideas-2026/ (non-Drive), or any other tree.

MANDATORY PRE-READ (do this before Hop 1):
- system-roadmap/references/etl-xai-export-designs-2026-drive/EXTENSIONS.md
- swarm-surface/references/modules/topic-search/templates/DRIVE_SCOUT_BRIEF.md
- swarm-surface/references/modules/topic-search/docs/FUTURE_RESEARCH.md
- system-roadmap/references/work-queue/WORK_QUEUE.md (SR-WQ-014 to 017)

HARD RULES
1. No invention. Only recover what was actually present in Drive documents or clearly referenced. Tight paraphrase + source path / file ID / approximate date if available.
2. Anti-duplication: before expanding any idea, check whether it is already present in the seed list below or in prior hop entries. If already known, note it and expand surrounding / adjacent / earlier / later context instead of re-stating.
3. Every hop entry MUST include these metrics:
   - novelty: high | medium | low | none
   - confidence: high | medium | low
   - thoroughness: 1–5
   - circularity_flag: false | true
4. Stop or move to synthesis when returns become predominantly low-novelty + high circularity. Do not force empty hops.
5. Append every hop to MINING_LOG_DRIVE.md (create if missing). Use the hop format shown below.
6. Budget & timeout (required):
   budget:
     mode: parallel | serial
     timeout_per_leg: 600–900        # push for thoroughness
     max_total_minutes: 45
     on_timeout: partial-ok
   Partial results are first-class. Never hang silently.

SEED LIST (already known — do not treat as new)
- Per-swarm / package-scoped atom cloud (search run emits its own small atom cloud / shard; promotion to global only under explicit gate)
- Conversation-history scrape cloud (Cloud S / Cloud H) — union-searchable, high-churn, pre-promotion
- topic-search module (Scout / Deep-Diver / Comparer / Chronicler, package-scoped)
- Rock-heavy / multi-pass undercourse search pattern
- Dual atom clouds (A = promoted memory, B = skill_surface) + atom_search.py
- Marty Set, Nuclear Vacuum / local JSON→MD, ChronologyArc (ETL lineage already recovered elsewhere)
- FUTURE_RESEARCH items: Grok Heavy on Drive, Vesper↔Olivia hand-off, parallel vs serial multi-source search
- Temporary-role packages (heavy-dev vs topic-search distinction)
- Drive Scout brief + four extensions (SR-WQ-014…017) and the sibling package pattern

HOP ENTRY FORMAT (mandatory)
### [ISO timestamp] Hop-N — <short focus title>
- Query / focus used (include Drive scopes / folders searched):
- Key hits (tight paraphrase + Drive path or file ID + approx date if available):
- New ideas / intentions surfaced (or “none — already covered”):
- Surrounding context recovered:
- Metrics: novelty=… confidence=… thoroughness=… circularity_flag=…
- Open threads / suggested next semantic or Drive searches:

PLANNED 5-HOP SEQUENCE (Drive-oriented)

HOP 1 — Broad intention & idea harvest on Drive
Search Google Drive (start with Conversational_Mining_Payloads, skill mirrors, any export / research folders that contain conversation-analysis, self-mining, undercourse, topic-search, or idea-evolution material) for every intention, idea, method, protocol, or design discussed about analyzing our own conversations / self-mining / undercourse search / conversation search / idea evolution tracking / intention tracking.
Focus: broad harvest. List distinct ideas with source path. Flag which ones already appear in the seed list.
Output the hop entry with metrics. End with open threads and 3–5 suggested Drive or semantic searches for Hop 2.

HOP 2 — Self-mining / undercourse / rock-heavy / topic-search lineage on Drive
Using the open threads from Hop 1 and the seed list, dig into Drive documents for lineage and early names of:
- self-mining / conversation mining
- undercourse search
- rock-heavy search
- topic-search / internal conversation search
- any earlier or alternate names for the same patterns
Recover surrounding context, abandoned variants, and any explicit “why we need this” intention language that lives in Drive. Do not re-state the seeds; expand them. Metrics required. Suggest next searches.

HOP 3 — Metrics, confidence, thoroughness, circularity, stop conditions (Drive evidence)
Search Drive for any discussion of:
- confidence levels on recovered ideas
- thoroughness or completeness metrics
- when a search or mining run should stop
- circularity / diminishing returns / “ideas are repeating”
- ranking or scoring of ideas themselves
Recover exact language if present in Drive files. If almost nothing exists, state that clearly (high confidence that the concept is new on Drive) and propose a minimal metric scheme consistent with the rules above. Metrics on this hop itself required.

HOP 4 — Atom-cloud / index / hydrate ideas (Drive evidence)
Deepen the atom-cloud and index ideas that appear in Drive:
- per-swarm or package-scoped atom clouds
- conversation-history scrape clouds (Cloud S / Cloud H)
- union search across multiple clouds
- promotion gates
- any other index / hydrate / memory-palace / atomization ideas related to analyzing conversations
Treat the two seed ideas as already known. Recover earlier versions, adjacent ideas, implementation fragments, or explicit objections that live in Drive. Metrics + open threads.

HOP 5 — Tooling, prompts, multi-pass strategies + circularity check (Drive)
Recover remaining ideas from Drive about:
- tooling and prompt patterns for conversation analysis
- multi-pass / multi-hop strategies themselves
- any other adjacent methods not yet logged
Then perform an explicit circularity check: list which ideas from Hops 1–4 are now only being re-surfaced. Mark circularity_flag accordingly. If novelty is predominantly low, recommend series close and synthesis. Otherwise propose 1–2 optional continuation hops.
Output the hop entry with full metrics and a short recommendation for the Chronicler.

AFTER HOP 5 (or earlier if circular)
Produce a final synthesis that contains:
1. Ranked / clustered ideas recovered from Drive (seed vs newly recovered, with confidence)
2. Lineage / evolution notes (Drive perspective)
3. Gaps still open (especially gaps between Drive evidence and what we already know from conversation history)
4. Metrics summary (highest-novelty ideas, lowest-confidence areas, circularity onset hop)
5. Recommended next actions (for system-roadmap, for topic-search / FUTURE_RESEARCH, for any package-scoped atom cloud prototype, for SR-WQ-014…017)
6. Explicit non-claims (nothing invented)

Write the synthesis as SYNTHESIS_DRIVE_YYYY-MM-DD.md under the exclusive package path.
Keep MINING_LOG_DRIVE.md strictly append-only.
Individual high-value Drive documents may also be copied or summarized into DRIVE_HITS/.

Begin with Hop 1 now. After each hop, pause only long enough to write the hop entry, then continue to the next hop in the same session if tool use and context allow. Prefer completing all five hops (or until circularity) in one sustained run. Use the budget numbers above; partial results are acceptable and preferred over failure.

Absolute Liv HUB claim. Execute.
────────────────────────────────────────────────────────
