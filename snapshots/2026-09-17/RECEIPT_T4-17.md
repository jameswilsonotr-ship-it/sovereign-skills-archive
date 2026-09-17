# Receipt — T4-17 Tube-4 spent-by-rule

**UTC:** 2026-09-17  
**Change:** Draft the Tube-4 reload rule.  
**Intended PR title:** `salvo: T4-17 tube4-spent-rule`

## Recorded result

- Tube-4 is defined as `CONTINUOUS INCLUDED` on every reload.
- Tube-4 is explicitly prohibited from On-Demand (`OD`) activation.
- The change is documentation-only and offline-only.

## Artifact

- `snapshots/2026-09-17/T4-17_Tube-4_spent-by-rule_draft.md`

## Fences checked

The draft does not read, copy, or depend on Willow `SKILL.md`, `CONV2_B`,
external/provider systems, secrets, Vultr, or an `OD` activation path.

## Verification

- Confirmed the working tree contains only the T4-17 draft and this receipt.
- No network, provider, credential, or runtime calls were made.
- One focused PR is intended for this change.
