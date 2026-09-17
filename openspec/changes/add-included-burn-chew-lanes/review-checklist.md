# Packet-PR review checklist

**Atom:** `atom-bc-03-packet-pr`
**Parent change-id:** `add-included-burn-chew-lanes`

Use this checklist for the one PR/reviewable unit that carries this atom.
The checklist is a gate: an unchecked item blocks approval.

## Identity and scope

- [ ] The PR description names exactly one atom:
      `atom-bc-03-packet-pr`.
- [ ] The PR description names the parent change-id:
      `add-included-burn-chew-lanes`.
- [ ] The PR changes only files required by this atom.
- [ ] The PR does not silently implement, edit, or depend on a sibling atom.
- [ ] The PR is independently reviewable, mergeable, and revertible.

## Sibling-coupling rejection

- [ ] I checked the diff for sibling atom identifiers, files, and
      requirements.
- [ ] I checked that the acceptance evidence does not require a sibling PR to
      be understood or reviewed.
- [ ] If sibling-coupled work was found, I rejected/returned this packet and
      requested a split into the sibling atom's own PR.

Do not waive these checks because the sibling change is small, convenient, or
already present locally. One atom is one PR.

## Chew completion and Meter Burn Desk handoff

- [ ] The packet's review chew is complete and all requested changes are
      resolved.
- [ ] I applied the repository's canonical Meter Burn Desk tag to the PR.
- [ ] The PR description or review note records the handoff and names both
      `atom-bc-03-packet-pr` and `add-included-burn-chew-lanes`.
- [ ] I verified that the tag is visible before marking the handoff complete.

If the chew is not complete, leave the Meter Burn Desk completion tag off and
keep the packet in review.
