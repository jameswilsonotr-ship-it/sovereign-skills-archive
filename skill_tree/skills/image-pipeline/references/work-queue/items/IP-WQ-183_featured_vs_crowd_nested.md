# IP-WQ-183 — featured vs crowd + nested-frame law

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** REEL.md characters section · IP-WQ-174

## Idea

Two extra rules the Short path never had to stress:

1. Cameo inflation. Parents and bridesmaids are not mouths.
2. Nested frames. A phone screen of Katy is not a third Katy.

## Reasoning

Hot N Cold is stuffed with readable faces: priest (comments even clock the judgy face), mom and dad, Shannon Woodward, Jadyn Maria, a mob of bat-brides, dancers, kids. Featured-mouth count without a law becomes a roster explosion.

The warehouse beat where Alexander pulls a phone and Katy is *on the screen* is a second copy of I, not Roman III. Same for reflections, TV inserts, posters.

Default: speaking / hunted / hunting / named in the lyric = featured. Everyone else = ignored. Nested picture of an existing Roman stays that Roman with `nested=true` on the beat.

## Work

- CHARACTERS.json `kind` stays candidate|splinter|agent. Add optional `featured: true|false` and beat flag `nested`.
- RUNBOOK one paragraph: count featured mouths before plates. Crowd is ignored. Nested copy does not mint.
- Smoke test: Hot N Cold featured count is 1, or 2 if she asks for Alexander. Never 8.

## Exit

RUNBOOK + schema note. Smoke card in 182 obeys the count. No extra candidates from cameos or screens.
