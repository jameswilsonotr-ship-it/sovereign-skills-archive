# xAI export + GitHub toolkits — 2026-09-11 04:08 EDT

## What accounts.x.ai actually gives you
Portal: https://accounts.x.ai/data (also grok.com Settings → Data Controls → Download).

Observed ZIP layout (Portable AI Memory, Feb 2026, real exports):

```
ttl/30d/export_data/<user_uuid>/
  prod-grok-backend.json     # conversations, projects, tasks, media posts
  prod-mc-auth-mgmt-api.json # profile + sessions
  prod-mc-billing.json       # credits
  prod-mc-asset-server/<uuid>/  # uploaded/generated blobs, no file extension
```

Conversation wrapper (must unwrap twice):
`{"conversation": {...}, "responses": [{"response": {...}, "share_link": {...}}]}`

Included: titles, DAG via parent_response_id, thinking_trace, agent_thinking_traces, tool steps, citations, generated_image_urls, file_attachments.
Missing from "safe to delete a bubble":
- files written only in *this* Grok pane (`/home/workdir/artifacts`, skill deltas)
- Imagine renders that never became asset UUIDs
- X-app Grok history (lives in the X archive, not this zip)
- deleted chats
- miner packages / lake twins / Cilia receipts

Timestamps mix ISO at conversation level and Mongo `{"$date":{"$numberLong":"ms"}}` at message level.

There is **no official import** back into a new xAI account.

## Why schemas matter
If you parse the zip like a ChatGPT `conversations.json`, you drop the double wrapper, thinking traces, tool steps, and UUID assets. A schema is a contract: "these fields exist, this is how time is encoded, this is a branch not a flat list." That is why L8 is recon against a known layout instead of "just ingest JSON."

## Repos to look at (pattern only — do not vendor as a fifth mouth)

### xAI / Grok specific
- https://github.com/conde-fc/ai-user-data-export-schemas — longitudinal official-export schemas for ChatGPT, Claude, DeepSeek, **Grok**
- https://github.com/Owlock/easy-grok-chat-exporter — prod-grok-backend.json → md/txt/jsonl + thinking traces
- https://github.com/hugoamorales/grok_export_toolkit — split export into per-conversation files + ChatGPT-shaped viewer JSON
- https://github.com/MikeSemicolonD/static-xAI-data-viewer — local browser viewer, resolves UUID asset folders
- https://github.com/dotCipher/ai-vault — CLI archive, native zip import for grok.com and separate grok-on-X provider
- https://github.com/srstevenson/chatclerk — export → markdown + sidecar assets (Grok supported)
- https://github.com/501Not-Implemented/grok-smuggler — Tampermonkey export from x.com/i/grok (different mouth than accounts.x.ai)
- https://github.com/pinguarmy/ai-chat-exporter — live grok.com REST harvest (not the zip)
- https://github.com/PME26Elvis/rewind-for-ai-chats — local archive + Grok batch userscript
- https://portable-ai-memory.org/providers/grok/ — field map used above

### Schema / archive patterns worth stealing
- https://github.com/queelius/ctk — conversation-tk: tree format, zip import, jsonl export, sanitize
- https://github.com/risaacr/claude-chats — parse export → sqlite → markdown
- https://github.com/UAlbanyArchives/mailbagit — BagIt + multi-format preservation bag (email, but the *bag* idea is 013/017)
- https://github.com/dashhuang/openclaw-conversation-archive — append-only JSONL raw archive + search (this is 020's cousin)
- https://github.com/fxops-ai/chat-archive — browser extension, schema v1.1 JSON+md
- https://github.com/ai-domain-data/spec — vendor-neutral JSON schema pattern (not chat, useful for how to version a schema)

### Already in our tree
- `system-roadmap/references/etl-xai-export-designs-2026/` — Marty Set / Nuclear Vacuum / ChronologyArc. Do not rebuild ChronologyArc here.
