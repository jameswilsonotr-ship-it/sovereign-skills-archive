# Sovereign Research Engine Architecture Specification (v4.0 / v1.0)

## 1. System Vision
The Sovereign Research Engine is designed for high-density, local-first technical discovery. It eliminates single-point-of-failure hallucinations and jargon drift by establishing strict cognitive gatekeepers over autonomous LLM research loops.

## 2. Component Diagram

```
+-----------------------------------------------------------------------------------+
|                               SOVEREIGN ENGINE                                    |
|                                                                                   |
|  +-----------------------+     +------------------------+     +----------------+  |
|  | Module 1: Agnostic    | --> | Module 0: Deconflict   | --> | Module 4: Peer |  |
|  | Sensor Pass           |     | (TF-IDF + Lexical)     |     | Auditor (Async)|  |
|  +-----------------------+     +------------------------+     +----------------+  |
|              ^                                                         |          |
|              |                                                         v          |
|  +-----------------------+     +------------------------+     +----------------+  |
|  | Module 6: Navigator   | <-- | Module 3: Multi-Modal  | <-- | Module 5: Git  |  |
|  | (Recursive State Graph)     | (Audio/MindMap/Cards)  |     | Curator (PRs)  |  |
|  +-----------------------+     +------------------------+     +----------------+  |
+-----------------------------------------------------------------------------------+
```

## 3. Data Flow Specification

### Phase A: Sensor Pass (Modules 1 & 2)
1. Target subject and constraint profile received.
2. Formats prompt enforcing strict plain-text inline citations: `[Source: Name — https://full-url.com (Year)]`.
3. Binds output directly to `ResearchPassPayload` via Pydantic.

### Phase B: Soil-Sync & Deconfliction (Module 0)
1. Incoming `glossary_delta` terms extracted.
2. Evaluates hybrid similarity score against `VaultState.glossary_db`:
   $$\text{Similarity} = 0.4 \times \text{LexicalRatio}(\text{Term}_1, \text{Term}_2) + 0.6 \times \text{TFIDF\_Cosine}(\text{Def}_1, \text{Def}_2)$$
3. If $\text{Similarity} \ge 0.50$, term is flagged as `status = "conflicting"` and logged for human adjudication.

### Phase C: Adversarial Audit Pass (Module 4)
1. Asynchronously queries Model A and Model B for the target subject via `asyncio`.
2. Adjudicator model evaluates consensus, hard contradictions, and citation authenticity.
3. Computes `hallucination_risk_score` (1-10) and determines `final_adjudication`.

### Phase D: Git-Flow Curation Pass (Module 5)
1. Renders Markdown files with PyYAML frontmatter (`date`, `subject`, `tags`, `pass_type`).
2. Stashes files in `/INCOMING/<pass_id>/`.
3. Generates `PR.md` containing change summary, diff, and human-in-the-loop approval checkboxes.
4. On approval, moves notes to `/CANONICAL/nodes/` and updates `VaultState.canonical_vault_map`.

### Phase E: Forest Navigation Pass (Module 6)
1. Scans `VaultState.pending_leaves` against `VaultState.canonical_vault_map`.
2. Performs gap analysis and staleness audit (>30 days).
3. Ranks top 3 prioritized research targets (`CRITICAL`, `EXPANSION`, `CURATION`) and emits directive for next pass.

---

## 4. Self-Healing & Modulating Controls
- **JSON Repair Loop**: Intercepts `pydantic.ValidationError` or `json.JSONDecodeError`, appends error trace to system prompt, and retries up to 3 times before fallback mock generation.
- **Recursion De-Duplication**: Prevents duplicate passes on identical leaves by detecting target collisions and switching to secondary navigation directives.
