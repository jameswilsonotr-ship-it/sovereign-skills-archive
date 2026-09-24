# Second Salvo Collision Scan

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-05-collision-scan` |
| Slot | `S2-05` |
| Base | `skill-tree-intake` at `cf7afbe782b7cc790aa3683c8d4268aa4ed29ba4` |
| Scan mode | Local, offline, read-only inventory |
| Scope | Included **Ultra** only |

## Result

**UNVERIFIED — the second-salvo plan was not present in the scan input.**

`docs/burn-wave/SECOND_SALVO_40.md` is not present in the checked-out base
tree, and no local branch or reachable commit contains that path. The base
tree also contains no S2 assignment registry. Therefore this pass cannot
honestly certify that the second-salvo assignments have no duplicate owner or
reserved-path collision.

This is a blocking evidence result, not a finding that the plan is clean.
Re-run this scan against the plan revision before accepting S2-05.

## Evidence inventory

The local base contains these burn-wave paths:

| Path | Relevance |
| --- | --- |
| `docs/burn-wave/corpora/MANIFEST.md` | Offline corpus manifest |
| `docs/burn-wave/corpora/MANIFEST.json` | Synthetic/offline corpus inputs |

The following expected scan input was absent:

| Path or source | Status |
| --- | --- |
| `docs/burn-wave/SECOND_SALVO_40.md` | Not present |
| S2 slot/owner registry | Not present |
| Other local second-salvo plan or assignment file | Not found |

The only path introduced by this change is this report:
`docs/burn-wave/SECOND_SALVO_COLLISION_SCAN.md`.

## Collision checks

| Check | Result | Basis |
| --- | --- | --- |
| Duplicate ownership across S2 slots | **UNVERIFIED** | No second-salvo assignments or owner fields were available |
| Duplicate ownership within S2-05 | **UNVERIFIED** | No S2-05 plan entry was available |
| Reserved-path collision | **UNVERIFIED** | No plan path reservations were available |
| Report-path collision | **NO COLLISION IN BASE** | The report path was absent before this change |
| Existing burn-wave corpus-path collision | **NO COLLISION IN BASE** | This change does not modify `docs/burn-wave/corpora/**` |

## Hard fences

These fences are binding for S2-05 and are not inferred to be satisfied by
the incomplete evidence:

- Included **Ultra** only.
- **OD is excluded**.
- Do not read, modify, claim ownership of, or reserve `Willow SKILL.md`.
- Do not read, modify, claim ownership of, or reserve `CONV2_B`.
- Treat **Vultr** and **Cold Steel** as distinct; neither is an alias for the
  other.
- No external calls. The scan uses only the checked-out repository.
- No secrets, credentials, tokens, or sensitive values belong in the plan or
  this receipt.
- Do not inspect, claim, or alter any other S2 slot as part of S2-05.

## Acceptance gate

S2-05 can move from **UNVERIFIED** to a collision verdict only when the exact
second-salvo plan revision is supplied locally. The follow-up scan must:

1. enumerate every S2 slot in that revision;
2. normalize owner identifiers and report any owner assigned to more than one
   slot;
3. enumerate every reserved path and report exact and normalized-prefix
   overlaps;
4. apply the hard fences above; and
5. record the plan revision and evidence paths in this report without making
   external calls or exposing secrets.

## Receipt

- Working tree scope: one new file under `docs/burn-wave/`.
- No other S2 slot was changed.
- No external service, API, or network source was used for the scan.
- No secret material was read or added.
