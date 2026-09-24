# Split-engine stress pack — NEW conversation only

Paste this as the first user message in a fresh Expert chat.

```
Olivia, Expert only. Liv HUB. Chatty mode.

Run image-pipeline split-engine stress pack IP-WQ-052.
Do not create a new skill. Do not use SAM.
Dump means inline render_file of kept jpegs.
Cap 2 people / 8 plates per turn.
Echo comments, Mira grades, you decide. Neither may stop keep_path.

Scripts you must call, not reinvent:
  inbound_classify.py
  segment_grid.py
  inbound_queue.py
  isolate_person.py
  split_plan.py
  emit_intent.py
  keep_path.py
  scaleback_loop.py
  hub_review.py
  smoke_split_engine.py

Turns:
1. Run smoke_split_engine.py. Paste the ok/fail JSON.
2. I will attach one single still. Menu C. Four plates. Keep each.
3. I will attach one pair. Isolate G and E. Show both intents. Four plates on the winner.
4. I will attach a 3-up. Queue three, process two, leave one in QUEUE.json.
5. I will attach a 2x2. Queue four, process two.
6. If any plate is a black box: keep disk if present, scaleback with implication, retry once.
7. Menu B on one crop: candidate card + four plates. kind=candidate.
8. Run hub_review on that candidate. Print mira.status and olivia_hub.decision.
9. Prompt bunny with no holographic ears. If Mira flags ears-required, proceed anyway and write the conflict down. Do not patch KNOWN_DNA.
10. Stop. Write STRESS_RECEIPT.md. Do not start architecture.

If a script is missing, say missing. Do not write a replacement skill.
```
