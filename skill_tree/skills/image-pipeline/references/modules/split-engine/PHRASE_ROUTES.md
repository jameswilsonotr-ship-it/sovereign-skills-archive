# Split-engine phrase routes

| Phrase | Route |
|---|---|
| process these / split these / four plates | inbound_classify → segment → queue → split_plan → emit_intent GENERATE_IMAGE |
| what did you send me this for | menu A WHY |
| make an agent out of this | menu B AGENT + still four-plate inline dump |
| agentify / agentify these / identify as agent | agentify subscale — menu B. Multi-frame set = one candidate. Bare `identify` is not a hit. |
| generate engine | menu C |
| overlay / merge / twister | menu D |
| dump / show me / inline | render_file kept jpegs interleaved. Not disk-only. |

| isolate / keep this person / crop her out | isolate_person.py dual G+E then split_plan |
| quad / 2x2 / four-up | layout grid2x2, four crops |
