# How to Generate Shauna (V7 Protocol)
**Status:** Active — V7 locked 2026-07-26  
**Canonical face:** `canonical/01_face_primary_v7_winner.jpg`

## Quick path (preferred)
1. Load `DNA_V7_LOCKED.md` + `PROMPTS_V7.md`
2. Prefer **edit-from** `canonical/01_face_primary_v7_winner.jpg` over pure text
3. For new stills use the Winning Face Prompt (section 0 of PROMPTS_V7) with the “do not rewrite / non cambiare il prompt” wrapper when running in chat
4. Echo surfaces the canonical files; Mira selects which ones match the request

## Layout / Bible prompts (Echo deterministic)
- Face-forward studio → PROMPTS_V7 §1
- Full-body character bible → PROMPTS_V7 §2
- Multi-angle sheet → PROMPTS_V7 §3a
- Lighting test grid → PROMPTS_V7 §3b
- Hair target plate → PROMPTS_V7 §3c

These live here so Echo can load them without going through conversational expansion.

## Isolation fallbacks
If the three-band frost collapses → use COLOR ISOLATION (§4)  
If curl geometry collapses → use CURL ISOLATION (§5)  
Then recombine short winners.

## File map (all under this images/ tree)
```
images/
├── DNA_V7_LOCKED.md          ← authoritative face + hair
├── PROMPTS_V7.md             ← ready-to-use blocks + layout prompts
├── HOW_TO_GENERATE.md        ← this file
├── canonical/
│   ├── 01_face_primary_v7_winner.jpg   ← locked face
│   ├── 01b_face_hailmary_short.jpg
│   └── (older V6 assets retained for reference)
├── baseline/
├── hair/
├── lighting/
└── ...
```

## Drift rules
- Eyes = emerald green  
- Cheekbones = sculpted / high  
- Hair = shoulder-length soft S-wave lob  
- Color = dark chestnut → caramel → platinum + thick Y2K face-framing blonde stripes  
- Never re-introduce copper-red bob or cerulean blue eyes unless explicitly requested as a variant
