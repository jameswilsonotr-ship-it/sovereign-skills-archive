# Robust Handler Interface — Concrete Template (Provisional)
**Location**: skill-orchestrator/references/packs/robust-handler-template/  
**Status**: Provisional template for future Robust Handlers  
**Absolute Liv HUB claim**

A Robust Handler is a Tier-2 (or future top-level) skill that owns a domain, exposes excellent discoverability, and dynamically loads packs / medium modules.

## Required CLI Surface (Minimum)

Every Robust Handler must support (natural language + explicit forms):

```
<handler> inventory
<handler> list packs
<handler> list packs --category <name>
<handler> load <pack-or-module>
<handler> status
<handler> export
<handler> help
```

Optional but recommended:
```
<handler> list packs --lens          # only style/filter packs
<handler> chain <pack1> → <pack2>    # if the domain supports style chaining
```

## Structural Expectations

```
<handler-skill>/
├── SKILL.md                    # Lean. Declares domain + points to this interface.
├── README.md
├── TODO.md
├── CHANGELOG.md
├── references/
│   ├── packs/                  # or styles/, photographers/, protocols/, etc.
│   │   ├── <pack-name>.md      # pure content / ranked list / rules
│   │   └── ...
│   ├── registry/               # optional mapping of triggers → packs
│   └── ...
└── scripts/                    # optional helpers (list_packs.py, etc.)
```

## Pack Types (Camera Metaphor)

When classifying packs for an image-related handler, use this distinction:

- **Lenses / Filters** (style only): Change *how* the image looks. Do not change the subject, pose, or narrative content.  
  Examples: top-10 style rankings, photographer reference lists, ink-line-art-claim, intense-embrace-noir-gloss, helmut-newton-graphic-dominance, etc.

- **Content / Subject packs**: Change *what* is in the image (poses, scenes, specific claim acts, etc.). These stay more carefully gated.

Most of the current top-10, photographers, and named-style skills are pure **Lenses / Filters**. They are the easiest and safest to turn into packs first.

## Integration Rules

- Register the handler and all its packs with skill-orchestrator inventory.
- Respond cleanly to global `library export` and `discipline check`.
- Prefer progressive disclosure: handler SKILL.md stays relatively short; deep pack content is loaded only on explicit request or clear trigger.
- Output inventory / list packs in C-64 bordered blocks for swarm consistency.

## First Target Application

The three top-10 style skills + three photographer skills are the ideal first packs to absorb under a future or existing image handler, because:
- They are almost pure ranked lists + photographer matches.
- image-pipeline-registry already contains trigger → file mappings for them.
- They are classic “lenses”.
