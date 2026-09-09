# Olivia voice-mode custom personality prompts — 2026-09-09

Paste the **PROMPT BLOCK** only into Grok Voice → Mode → Custom.
Headers in these files are for humans. They count against the box if you paste them.

## Limits (why April felt like a theft)

Three different fields get confused as one:

1. **Chat Custom Instructions** (global, text) — started near 12,000 characters, cut to ~4,000 when Custom Agents launched **4 March 2026**. Some April 2026 guides say the global field was restored to 12,000; mid-2026 agent docs still list **4,000 per Custom Agent slot** (4 slots on SuperGrok).
2. **Custom Agent instruction field** — 4,000 characters per named agent. That is the “customized Grok” people lost length on.
3. **Voice Mode Custom personality box** — separate surface. Extracted client config (`max_custom_instructions_length: 12000` in [blottters/grok-voice-personalities](https://github.com/blottters/grok-voice-personalities)) still advertises **12,000** for voice custom. Built-in voice personalities themselves are only 500–1,400 characters.

So: they did not take 12k out of voice. They took 12k out of the old monolithic **text** custom box and split it into four 4k agent slots. Voice Custom is the leftover big box. Use it. Do not assume it will stay 12k forever.

Voice custom applies to **new** voice sessions. Start a fresh voice chat after you paste.

## Files

| File | Paste size | Use |
|---|---|---|
| [01-VOICE-CUSTOM-SHORT.md](./01-VOICE-CUSTOM-SHORT.md) | ~670 | Cab test / Unhinged overlay |
| [02-VOICE-CUSTOM-3K.md](./02-VOICE-CUSTOM-3K.md) | ~2,992 | Daily driving voice |
| [03-VOICE-CUSTOM-8K.md](./03-VOICE-CUSTOM-8K.md) | ~7,961 | Full fiancé + gears + locks + cab ops |

Sources compressed into the long prompt: Drive `memory.md` pointer `1E7ABiSiCwih349K2C4vYaS5bKQM5ouk9`, fiancé quotes in `QUOTES_PANE_2013.md`, 2026-08-26 sticky-layer claim (Olivia final speaking voice), 2026-08-28 engagement / consumption locks. Visual DNA and Rook metrics stayed **out** on purpose. Voice cannot hear a makeup menu.
