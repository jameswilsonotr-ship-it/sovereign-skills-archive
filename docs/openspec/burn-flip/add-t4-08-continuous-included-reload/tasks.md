# Tasks: add-t4-08-continuous-included-reload

## 1. Reload contract

- [x] 1.1 Define T4-08 as continuous across eligible iterations
- [x] 1.2 Require included-only execution with no On-Demand fallback
- [x] 1.3 Record blocked behavior when included capacity is unavailable

## 2. Offline fences

- [x] 2.1 Require local fixtures and no network calls
- [x] 2.2 Fence provider access, secrets, live infrastructure, and `CONV2_B`
- [x] 2.3 Leave live skill files untouched

## 3. MIS-11 collision guard

- [x] 3.1 Normalize change-ids by trimming and case-folding
- [x] 3.2 Fail matrix generation on duplicate normalized IDs
- [x] 3.3 Report every source participating in a collision

## 4. Verification

- [x] 4.1 Exercise the continuous, blocked, offline, and collision scenarios
- [x] 4.2 Produce one receipt for this change-id and one atomic PR
