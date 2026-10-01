# IP-WQ-189 — knowledge-graph confirm pass

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-175 · IP-WQ-179

## Idea

After resolve, confirm director / year / runtime / featured names from Wikipedia videography, MusicBrainz, IMVDb. Use it to check the search hit. Do not use it to invent frames.

## Reasoning

Title search can still pick a lyric video or a live. Hot N Cold’s public record is thick: Alan Ferguson, 2008, Alexander Francis Rodriguez, parents as extras, First Christian Church, ~4:43. A confirm pass that checks duration and “official music video” + director match is cheap insurance.

This is research, not SOURCE. A Wikipedia still may feed 181 only if it is a real public still and labeled `source=wiki`.

## Work

Manual is enough for v0: Olivia fills a CONFIRM card on famous tapes. Later a thin MusicBrainz lookup is optional (`musicbrainzngs`). No scraping of licensed galleries into the lake as if we own them.

## Exit

182 smoke includes a confirm block (director, year, groom name, cameos=ignored). Resolver can run without this ticket. Confirm is a quality gate, not a fetch.
