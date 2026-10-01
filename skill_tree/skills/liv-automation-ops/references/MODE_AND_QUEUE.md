# Modes and automation queue — 2026-09-03

## How Auto picks

Public UI copy: Auto = "Chooses Fast or Expert."
xAI has not published the router rule. Treat Auto as a router you cannot inspect.
Fast = light / low latency.
Expert = single-thread deeper reasoning. Good for Drive publish + dual write.
Heavy = multi-agent team. Good for corpus mine. Connector cannot set it.
Build = separate surface (Grok Build). Do not route Liv jobs there.

Automation docs (x.ai/news/grok-automations): each job can pick a mode when you save it. Run now opens a real conversation. Mode lives on that conversation's dropdown, not in the prompt text. Prompt saying "dropdown = Expert" is a reminder to the operator, not a force.

When we `automation_update` the prompt, the UI can snap the mode picker back to Auto. That is the "went back to auto" hit. Re-set Expert after every prompt rewrite.

## Queue

Official: Run now / schedule / email trigger.
Known failure: runs stick in Queued (X 2026-07-24, platform delay). execTime = -1 and no status field = queued, not generating.
Do not stack Run now on a job that already has an execTime=-1 row from the last ten minutes.

## 2026-09-03 20:12 board

S1-S6: no Expert result yet. Fired 20:12.
S7: two queued rows 00:09/00:10 UTC. Do not fire again.
B1: one queued.
B2: two queued.
B3: four queued.
B4: two queued.
B5: one SUCCESS 00:05-00:12 + one extra queued.
B6: SUCCESS 00:05-00:11.
COMPARE: do not fire until skill-tree corpus exists.
