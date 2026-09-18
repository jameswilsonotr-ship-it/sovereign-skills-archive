# IP-WQ-177 — PERSONA lives on CHARACTER

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-174 · character.schema.json

## Idea

Do not create `persona.schema.json` as a fifth navy. Extend CHARACTER with thin fields that say what the person is *doing in the tape*.

## Reasoning

Bunny asked “what about persona?” The trap is minting a new object type every time a video has a role. Lead / foil / chorus-body / object is a relation to the song, not a new mouth.

Hot N Cold proof:
- I Katy = lead. Lyric job: names the flip and hunts it.
- II Alexander = foil. Lyric job: *is* the flip.
- Bat-brides = chorus-body, ignored unless she points.
- Zebra = object / prop.

Culture already bends wardrobe and pose (SKIN_CULTURE.md). Persona must not mint a mouth and must not guess nation.

## Work

Add optional fields to `character.schema.json`:

```json
"role_in_tape": { "enum": ["lead", "foil", "chorus-body", "object", "unspecified"] },
"lyric_job": { "type": "string" },
"relations": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["to", "rel"],
    "properties": {
      "to": { "type": "string" },
      "rel": { "type": "string" }
    }
  }
}
```

Default `unspecified`. Required set does not change — old inbound still validates.

## Exit

Schema bump documented in agentify CHANGE-adjacent note or module SKILL. No new file type. No mint from role.
