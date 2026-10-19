# Skin, hair, culture, feed

IP-WQ-098 + IP-WQ-130 · schema lock 2026-09-04
Parent: IPQ-070 · character.schema.json

Observed on the still. Not a race menu. Not a nation stamp.
Culture bends wardrobe and pose. It does not mint a mouth.
Geography lives in COVERAGE.md. Do not put continents here.

## Skin.tone (depth)

`alabaster` · `fair` · `light-olive` · `light-medium-warm-brown` · `medium-olive` · `rich-deep-brown` · `onyx` · `unspecified`

- `alabaster` = cool porcelain / goth-white. Not albino.
- `unspecified` does not default to fair.
- Mixed = observed notes, not a stew token.

## Skin.undertone

`cool` · `warm` · `olive` · `neutral` · `unspecified`

## Hair.family (cut / shape)

`pixie` · `undercut` · `short` · `bob` · `shoulder` · `long-straight` · `long-wave` · `coils` · `loc-short` · `loc-long` · `bun` · `unspecified`

## Hair.color

`alabaster-white` · `blonde` · `strawberry` · `copper` · `auburn` · `red` · `brown` · `dark-brown` · `black` · `silver` · `unspecified`

Red / freckle are hair+skin vectors, not races.
Hair-color hop on heat (dark → blonde) = fail. Edit from locked A.

## Scout vs token

Tone + hair.family + hair.color lock the form.
Coverage region is a separate scout bias: prefer empty slots when she has a still.
A region is not a tone. `onyx` is not Africa. `fair` is not Nordic.

## JSON

```json
{
  "skin": { "tone": "unspecified", "undertone": "unspecified", "observed": false },
  "hair": { "family": "unspecified", "color": "unspecified", "observed": false },
  "culture": { "tags": [], "influence": ["wardrobe", "persona-style"], "notes": "" },
  "feed": { "platform": "yt-still|yt-community-post|dump", "locale": "", "aesthetic_family": "" }
}
```

Fails: bleach · recast · costume-as-ethnicity · chrome-as-culture · hair-hop
