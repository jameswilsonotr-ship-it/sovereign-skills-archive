# Tasks: third-salvo-37-tube3-spent-rule

## 1. OpenSpec contract

- [x] 1.1 Declare slot `T3-37` and exact change-id
- [x] 1.2 Define `included-ultra` as the only eligible execution class
- [x] 1.3 Define On-Demand and ambiguous-class rejection

## 2. Spent-by-rule accounting

- [x] 2.1 Require exact change-id and one atomic PR
- [x] 2.2 Require complete OpenSpec artifact and post-land receipt
- [x] 2.3 Keep rejected or incomplete units `not-spent`

## 3. Fences and verification

- [x] 3.1 Record offline-only operation
- [x] 3.2 Fence Willow `SKILL.md`, `CONV2_B`, external/provider services,
  secrets, Vultr, and Linear
- [x] 3.3 Exercise the ADDED scenarios in
  `specs/tube3-spent-by-rule/spec.md`

Verification is documentation-only. No quota, billing, network, provider, or
runtime action is performed or claimed.
