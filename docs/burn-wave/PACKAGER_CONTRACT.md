# S2-31 packager contract

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-31-packager-contract` |
| Slot | `S2-31` |
| Inclusion profile | **Ultra only** |
| Deliverable | `docs/burn-wave/PACKAGER_CONTRACT.md` |
| Operating mode | Deterministic and repository-local |
| Installation policy | No installs, upgrades, or dependency resolution |

This document defines the packaging boundary for the included Ultra burn-wave
surface. It is a contract and validation recipe, not a packaging
implementation. The contract must remain reviewable as one atomic slice.

## Boundary

The packager may consume only an explicitly enumerated set of repository-local
files for the active slice. The file list is part of the input, not a
discovery result:

- paths are repository-relative POSIX paths;
- each path is under the declared burn-wave surface;
- each file is read as its checked-in bytes; and
- the list is sorted lexicographically before any digest or archive operation.

The packager must reject a path that is missing, outside the declared
allowlist, a symlink, or a directory. It must not walk the repository to find
additional material. An empty or ambiguous file list is a rejected package,
not an instruction to broaden the boundary.

## Package identity and outputs

The package identity is the tuple `(change_id, slot, inclusion_profile)`.
For this slice that tuple is:

```text
second-salvo-31-packager-contract / S2-31 / ultra
```

If a package is emitted, it consists only of:

1. the declared source files;
2. a manifest containing the exact sorted paths and SHA-256 for each source
   file; and
3. a receipt containing the package identity, manifest digest, validation
   result, and changed-path list.

The manifest and receipt are metadata about the package. They must not be used
to smuggle in files that were not in the declared source list. A package is
invalid if its manifest, receipt, or payload changes after validation.

## Determinism rules

Two runs with the same checked-in source bytes and the same declared file list
must produce byte-identical manifests, receipts, and package archives:

- preserve file bytes; do not insert timestamps, hostnames, usernames,
  temporary paths, random identifiers, or environment-dependent values;
- encode text metadata as UTF-8 with LF line endings;
- sort paths and manifest records lexicographically;
- calculate SHA-256 from the exact source bytes;
- if an archive is used, set a fixed timestamp, owner/group, permissions, and
  entry order; and
- use no network, package index, subprocess, provider, or live connector.

The package digest is computed over the canonical manifest bytes, after all
source hashes and metadata have been validated. A validation failure produces
no successful receipt and never falls back to a broader package.

## Validation

Validation is standard-library-only and must not install anything. A reviewer
must be able to prove the following locally:

1. The metadata identifies `second-salvo-31-packager-contract`, `S2-31`, and
   **Ultra only**.
2. The declared paths are unique, sorted, repository-relative, and inside the
   boundary.
3. Every source hash is the SHA-256 of the exact checked-in bytes.
4. Repeating the manifest and digest calculation without changing inputs gives
   the same bytes and values.
5. No OD, live skill-tree content, external service access, or dependency
   installation is needed or attempted.
6. The changed-path set for this slice contains exactly
   `docs/burn-wave/PACKAGER_CONTRACT.md`.

The focused repository checks are:

```bash
git diff --check
python3 - <<'PY'
from pathlib import Path

path = Path("docs/burn-wave/PACKAGER_CONTRACT.md")
text = path.read_text(encoding="utf-8")
required = (
    "second-salvo-31-packager-contract",
    "S2-31",
    "Ultra only",
    "No installs",
    "no OD",
)
missing = [phrase for phrase in required if phrase.lower() not in text.lower()]
if missing:
    raise SystemExit(f"missing contract markers: {missing}")
print("packager contract markers: ok")
PY
```

These checks inspect the contract only; they do not fetch, install, build, or
publish a package.

## Hard fences

- **Included Ultra only:** OD is excluded and must not be copied, indexed, or
  inferred into this package.
- No Willow `SKILL.md` content is added, copied, or changed.
- No `CONV2_B` surface is included.
- Vultr and Cold Steel remain distinct labels; neither is a packaging alias for
  the other.
- No external calls, credentials, tokens, secrets, unredacted payloads, or
  live connector/provider access.
- No package installation, dependency upgrade, lockfile rewrite, or network
  resolution.
- This slice changes only `docs/burn-wave/PACKAGER_CONTRACT.md`; it does not
  implement a packager or modify another S2 slot.
