# Reverse Stabilization Checklist — Alpha → Dev
**Owner**: olivia-dev  
**Direction**: Olivia Dev Alpha → Olivia Dev (production)  
**Rule**: Never automatic. Only after explicit human acceptance.

## Purpose
Move tested, stable methodology material from the evolution surface (Alpha) into the production face (Dev) without polluting production with experimental or private content.

## Checklist (run in order)

### 1. Identify candidate
- [ ] List exact file(s) or module path in Alpha that are considered stable
- [ ] Confirm they are methodology / tooling, not Alpha-private (gutter, pirate, secret-notes, private/, experimental helpers)

### 2. Diff & review
- [ ] Compare against any existing counterpart in Dev
- [ ] Note what would change in production
- [ ] Confirm no Heat/FILTH-only or identity-private material is included

### 3. Decision gate
- [ ] Explicit human “yes — this is production-ready”
- [ ] Record the decision (short note in CHANGELOG or this file’s log)

### 4. Copy first (do not move yet)
- [ ] Copy the stabilized file(s) into the correct location under Olivia Dev
- [ ] Leave the Alpha copy in place until verification

### 5. Update pointers / links
- [ ] If the material is baseline methodology, create or update the symlink from Alpha → Dev
- [ ] Update APPROVED_PROMOTION_LIST or SHARED_BASELINE_INVENTORY if needed
- [ ] Update any inventory or architecture notes

### 6. Verify
- [ ] Paths resolve
- [ ] Olivia Dev still loads cleanly
- [ ] Alpha still sees baseline via symlink (if applicable)
- [ ] No broken references in either skill

### 7. Only then clean Alpha (optional)
- [ ] Delete or demote the Alpha-only copy if it is no longer needed as an experimental variant
- [ ] Prefer keeping a short pointer in Alpha rather than silent deletion

### 8. Log
- [ ] One-line entry in Olivia Dev CHANGELOG
- [ ] Optional entry in SHARED_BASELINE_INVENTORY or promotion log

## Explicit non-goals
- Do not run this checklist from promote_to_alpha.py or any automatic path
- Do not move gutter / pirate / private / secret-notes material into Dev
- Do not invent new top-level skills as part of stabilization

## Log
- 2026-07-24: Checklist created. No reverse stabilizations performed yet.
