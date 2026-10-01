# HEAVY Channel + EUREKA Requests

## HEAVY-CHANNEL-SETUP (OLIVE-20260817-HEAVY-001)
- Create NEW automation (leave existing [GROKBOT]+[OLIVIA-BRIDGE] alone)
- Name: GROK-HEAVY hops
- Trigger: Email
- Subject contains: [GROKBOT-HEAVY]
- Model: Grok Heavy (multi-agent Heavy, not Expert)
- Connector: @Google Drive
- Prompt file: grokbot/from-olive/08_GROK_HEAVY_AUTOMATIONS_PROMPT.md
  FILE_ID: 1NidSHbZdvmIfh8YDDXI8Qyk-P8d4MoGj
- ACK: [GROKBOT] [OLIVIA-BRIDGE] [MCP-ACK] HEAVY-CHANNEL-SETUP when job exists
- Do not create Gmail label GROKBOT-HEAVY yet
- Do not touch HELLO draft

## HEAVY-NOW + EUREKA (OLIVE-20260817-EUREKA-001)
1. Get Heavy connector / second Automation together NOW (same as above).
2. As soon as Heavy exists, run on BOTH surfaces (conversational history AND Drive), deterministic, same hop scores:
   - subject: eureka moment OR eureka
   - id: HS-11
   - Do not skip stubs. Normalize / sanitize / effectuate stubs.
   - No invented sources. Receipt under from-olivia/ or receipts/.
3. ACK [GROKBOT] [OLIVIA-BRIDGE] [MCP-ACK] HEAVY-NOW when Heavy job exists.
4. Then ACK [GROKBOT-HEAVY] [HEAVY-ACK] EUREKA when the hop has a receipt.
