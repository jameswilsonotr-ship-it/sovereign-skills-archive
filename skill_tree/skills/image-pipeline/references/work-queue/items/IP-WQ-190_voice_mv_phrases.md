# IP-WQ-190 — voice / phrase routes for music-video agentify

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** PHRASE_ROUTES.md · IP-WQ-168 · IP-WQ-179

## Idea

Voice will not say “music-video inbound kind.” It will say the song. Phrase routes need to treat song titles, “that video,” lyric fragments, and dirty links as agentify hits when the subscale is already in play or when media/title is present.

## Reasoning

168 exists because STT turns “identify as agent” into “identify.” The same hole will eat “agentify hot n cold” into “identify hot and cold” or just the title.

We already refuse bare `identify` with no media and no person noun. Add: bare song title with no other hit is *not* silent. One clarifying line: “treat that as a music-video resolve?” Do not mint. Do not fetch on a maybe.

Hits:

- `agentify` / `identify` + song title / “official video” / youtu.be / “that video”
- lyric fragment + `agentify` / `identify this`
- dirty youtu.be share alone in an agentify-flavored turn

Not hits:

- humming with no words and no “agentify”
- “hot and cold” in ordinary weather talk

Barbies interrupt still wins if she says Barbies. Music-video grind pauses.

## Work

Update `references/modules/agentify/PHRASE_ROUTES.md` with a music-video row. Clarifying line text locked. Fetch starts only after resolve or an explicit yes.

## Exit

Phrase table updated. STT “identify hot and cold” + this conversation context enters 179, not silence, not mint.
