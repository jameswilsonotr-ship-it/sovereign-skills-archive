# Receipt — T4-26 continuous included reload

- UTC: 2026-09-17T09:49:00Z
- CINC target: `MIS-11`
- PR title: `salvo: T4-26 mis11-land-path`
- Delivery: one PR with this receipt as the reviewable unit
- Mode: offline OpenSpec only

## Contract

T4-26 continuously reloads the included path. Every reload remains on
included usage; On-Demand is forbidden and MUST NOT be selected as a fallback,
retry path, or overflow path.

The reload behavior is documentation-scoped in this receipt. No live reload,
provider request, spend action, or external-system write was performed.

## Land path

1. This receipt is the source artifact for the `MIS-11` CINC target.
2. Review and land it through the single PR named above.
3. Treat the landed receipt as the offline OpenSpec handoff; no second PR,
   external ticket mutation, or provider-side follow-up is implied.

## Fences

- No Willow `SKILL.md` or skill-tree live-lock changes.
- No `CONV2_B` unpack or use.
- No external or provider calls.
- No secrets, credentials, tokens, or connection strings.
- No Vultr work.
- No Linear mint or mutation.
- No On-Demand usage or spend.

## Verification

- [x] The scope is one receipt and one PR.
- [x] The contract explicitly requires continuous included reload.
- [x] On-Demand is explicitly forbidden, including fallback and retry paths.
- [x] The requested offline/OpenSpec fences are recorded.
