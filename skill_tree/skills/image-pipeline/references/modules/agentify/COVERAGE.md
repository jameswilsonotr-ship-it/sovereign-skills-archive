# Earth coverage — scrape + form grade

IP-WQ-099 · 2026-09-03 01:49 EDT  
Parent: IP-WQ-098 skin/culture/feed · IP-WQ-096 platonic forms · IPQ-070

## What “DEI” means here

Promote **coverage**, not a second navy of raced agents.

The live feeds will over-represent whoever Bunny saves (often US/EU/EN YouTube and gym stills). Archetype detection that only sees that dump will lock forms pale and coastal. The fix is a visible earth ledger: every region is a **slot to cover with packs and form-splinters**, not a seat to mint.

- One form may carry many regional wardrobe / persona-style splinters.
- A new region does not mint a new mouth.
- Unspecified tone is **not** fair. Compose must not default white when `skin.tone=unspecified`.
- Do not guess nation or blood from a face. Tag region from setting, dress, language, or her note.
- Antarctica is research-only. No plate quota.

## Slots (coverage, not people)

| Continent | Regions (fill, do not invent women into them) |
|---|---|
| Africa | Maghreb · West · East · Central · Southern |
| Asia | Levant · Gulf · Persia · Central · South · SE · East |
| Europe | Nordic · West · East · Mediterranean |
| Americas | Turtle Island / US-CA · Mexico-Central · Caribbean · Andes · Southern Cone · Amazon |
| Oceania | Australia · Polynesia · Melanesia · Micronesia |

Status per slot: `empty` · `pack-only` · `form-held` · `feed-heavy` (over-represented in inbound).

## Scrape fields

```json
{
  "coverage": {
    "continent": "",
    "region": "",
    "slot": "empty|pack-only|form-held|feed-heavy|unspecified",
    "observed": false
  }
}
```

CLI: `--continent` `--region`

## Grade hook

When judging a still against a form, ask:

1. Does this still only exist because the feed is one-region-heavy?
2. Is there an empty slot this pack could cover without recasting the form?
3. Would accepting it bleach or recast (098 fail) in the name of “diversity”? If yes, reject. Coverage never overrides tone-hold.

## Compose hook

If inbound dump is `feed-heavy` on one slot, next candidate pick should prefer an `empty` or `pack-only` slot **when she has stills for it**. Do not hallucinate a region to fill the chart.
