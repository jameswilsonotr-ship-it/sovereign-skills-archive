# AAR note — T3-34 meter fold (post-reset)

- **Change ID:** `third-salvo-34-aar-meter-fold`
- **Salvo / slot:** `third` / `T3-34`
- **Window:** post-reset
- **Baseline:** `0` at the reset boundary
- **Included:** `Ultra` only
- **Excluded:** `On-Demand`, unknown, and unclassified records

## Result

The post-reset fold is defined as an offline count of explicit `Ultra`
records for `T3-34`. `On-Demand` is excluded unconditionally; it is not
converted to `Ultra`, used as a fallback, or allowed to affect the included
meter.

No event sample or reset timestamp was supplied with this documentation-only
change, so this note records the post-reset rule and baseline rather than
asserting a runtime count. A future local AAR run can fill in the observed
post-reset record count without changing the eligibility rule.

## Boundary checks

- Pre-reset records do not carry into the post-reset fold.
- Records without an explicit classification are not promoted to `Ultra`.
- The fold needs no external/provider/secrets/Vultr/Linear access.
- This note does not modify `Willow SKILL.md` or `CONV2_B`.
