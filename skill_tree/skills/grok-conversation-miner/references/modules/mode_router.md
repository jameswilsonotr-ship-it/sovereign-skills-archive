---
name: mode_router
version: 0.1.0
owner: grok-conversation-miner
queue: GCM-WQ-023
status: live
stamp: 2026-09-11 04:37 EDT
---

# Heavy vs Expert — operator switch

Do not guess. Look at the pane.

## You are in HEAVY if
- Teammates are named (Harper, Benjamin, Lucas, or "agent 123")
- `chatroom_send` / team chatter exists
- Tool calls bounce with "another agent already completed"

## You are in EXPERT if
- No teammate chatter
- Solo tool list
- Drive `upload_artifact` / `download_artifact` are reachable

## What to do
| Need | If Heavy | If Expert |
|---|---|---|
| Binary Drive upload / hash roundtrip | Stop. Tell Bunny: switch me to Expert. Do the rest of the thinking here. | Do the upload. |
| Zip the whole queue, parallel research, four-way split | Stay. Split work. | Tell Bunny: switch me to Heavy if this is a multi-front grind. |
| `conversation_search` | Use it. Do not panic. | Use it. Do not panic. |
| Live sunset / vacuum | Still needs a named bubble + go | Same |

Never upload from Heavy "just in case." Never refuse Expert upload because yesterday Heavy could not.

Silly Bunny line (allowed): "You're in Heavy. I can write the receipt and the script. Flip me to Expert to push the tar."
Vice versa: "You're in Expert. I can push the tar. Flip me to Heavy if you want the four-way zip."
