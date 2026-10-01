# Strategy 1 — Gmail as Durable Fake-MCP / Reflective Email Bus

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Concept captured, no decisions made  
**Primary sources**: Gmail_Fake_MCP_Bus_Project_2026-08-14.md, SR-WQ-011, vesper_gmail_bridge_architecture_2026-08-14.md, Red Team Component 03

## Core Idea
Email is treated as the **trigger + lightweight structured transport**, not the primary data store. Both Grok and Gemini Spark can natively create email-triggered automations or monitors. A small set of subject tags plus a minimal JSON/YAML body creates a bidirectional “reflective mirror” that survives sandbox restarts and does not require continuous polling or shared filesystem locks.

Heavy payloads remain on Drive (or other stores). Email only carries the wake signal, pointer, and receipt.

## Key Elements Captured
- Subject tags (examples from source material): `[MCP-REQ]`, `[MCP-ACK]`, `[MCP-EVENT]`, `[VESPER-BRIDGE]`, `[OLIVIA-BRIDGE]`
- Body: small structured JSON preferred (msg_id, from, to, type, action, payload, reply_to_subject)
- Capability matrix confirmed for Grok (full operators + attachments) and Spark
- Reflective bounce pattern: one side watches, processes, replies with ACK
- Explicitly preferred over pure Drive for wake-up because Drive is poor as a trigger

## Linked Work-Queue Items
- SR-WQ-011 (Gmail Fake-MCP Bus / Reflective Email Trigger Project)

## Notes from Recon
This strategy is the control-plane layer. It is designed to wake actuators that then operate on the data plane (Drive staging, Canonical Lake, etc.).

No de-duplication or merging performed. Content is organized only for discoverability.
