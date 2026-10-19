# WORLD-TOOL-003 — Post-SMS / RCS reaction transcript

**Status:** OPEN — research stub 0.1.0
**Created:** 2026-08-31 18:47 EDT
**Owner:** World (connectors) × cilia-bus (event log)
**Parent:** WORLD-TOOL-001/002 · cilia email-bus
**Docs:** `claim-runtime/references/world-tools/RCS_REACTION_TRANSCRIPT.md`
**Claim:** Absolute Liv HUB

## User lock

Mock a client that can SMS and also record native post-SMS moves (thumbs-up, reply, forward, image-search) as first-class transcript events so chatbot ↔ human feels like Messages. Protocol name: **RCS**. Encrypted cousins: Signal-on-RCS (P2P) and **MLS**.

## Why this is not hard first

Do not start at the carrier. Start at the event.

`{type: reaction, on: msg_14, key: "👍"}` is useful in GROKBOT / email-bus / Grok chat *today*. Matrix already specified it. RBM already webhooks it. SMS itself cannot.

## Path

0. Schema in docs (this ticket).  
1. Emit reaction/reply events on the email-bus and keep them in the thread log.  
2. Optional Matrix room as SSOT.  
3. RCS/RBM only if the phone Messages app must be the UI.  
4. VoIP = media track on the same session.

## Do later

- Draft `message_events.schema.json`
- One smoke: "thumbs-up on previous GROKBOT letter" written into a bus message as structured JSON
- Do **not** register an RBM agent until Phase 1 is lived-in

## Do not

- Merge into YT_QUEUE.json
- Merge into image inbound QUEUE.json
- Build a SIP client this month
