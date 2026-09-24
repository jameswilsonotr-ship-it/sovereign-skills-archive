---
id: second-salvo-16-drive-contract
title: Drive connector contract
status: proposed
slot: S2-16
scope: included-ultra-only
tags: [burn-wave, connector, drive, offline]
---

# Drive connector contract

This document is the S2-16 contract for the included Ultra surface. It
describes the repository's deterministic Drive test double, not a Google Drive
integration.

## Scope and hard fences

- Included: Ultra only.
- Excluded: OD, Willow `SKILL.md`, and `CONV2_B`.
- Vultr is not Cold Steel; neither label changes this connector contract.
- No live Drive or other provider calls are permitted.
- No credentials, tokens, or other secrets are part of the contract.
- This change does not modify or claim any other S2 slot.

## Contract boundary

The implementation boundary is
`harness/src/sovereign_harness/connectors.py::DriveConnector`. It inherits
`AccountBoundConnector`, so every call is explicitly scoped to a non-empty
`account_id`:

```text
DriveConnector(account_id=<account id>)
```

The accepted account ID form is an ASCII identifier of 1–128 characters:

```text
[A-Za-z0-9][A-Za-z0-9._-]{0,127}
```

Surrounding whitespace is rejected. The connector never reads credentials and
never opens a socket.

### Operations

| Operation | Inputs | Result |
| --- | --- | --- |
| `list_files` | `folder_id: str \| None = None`, `query: str \| None = None`, `limit: int = 20` | A stable call envelope containing the request and the Drive fixture |
| `get_file` | `file_id: str` | A stable call envelope containing the request and the Drive fixture |

Inputs are keyword-only. The current contract records the request values as
given; it does not promise provider-side filtering, pagination, mutation, or
file-content download.

### Result envelope

Every operation returns a dictionary with this shape:

```json
{
  "connector": "drive",
  "operation": "list_files",
  "account_id": "drive-test",
  "request": {
    "folder_id": "fixture-folder",
    "query": "MIS-6",
    "limit": 3
  },
  "data": {
    "source": "offline-fixture",
    "files": [
      {
        "id": "fixture-drive-001",
        "name": "MIS-6 fixture note.md",
        "mime_type": "text/markdown"
      }
    ]
  }
}
```

`connector`, `operation`, `account_id`, and the request fields are
deterministic. The fixture source is always `offline-fixture`; its checked-in
shape is defined by
`harness/src/sovereign_harness/fixtures/drive.json`. The envelope is a
description of a call, not evidence that a provider was contacted.

## Offline acceptance cases

These cases are the acceptance contract. They can run without network access,
Drive authorization, a provider SDK, or secrets.

### A1 — account scope is mandatory

```python
import pytest
from pydantic import ValidationError

from sovereign_harness.connectors import DriveConnector

with pytest.raises(ValidationError):
    DriveConnector()
```

Also reject `account_id=""`, whitespace-only IDs, IDs with surrounding
whitespace, and IDs outside the documented character or length rule.

### A2 — list call shape is stable

```python
response = DriveConnector(account_id="drive-test").list_files(
    folder_id="fixture-folder",
    query="MIS-6",
    limit=3,
)

assert response["connector"] == "drive"
assert response["operation"] == "list_files"
assert response["account_id"] == "drive-test"
assert response["request"] == {
    "folder_id": "fixture-folder",
    "query": "MIS-6",
    "limit": 3,
}
assert response["data"]["source"] == "offline-fixture"
```

### A3 — get call shape is stable

```python
response = DriveConnector(account_id="drive-test").get_file(
    file_id="fixture-drive-001",
)

assert response["connector"] == "drive"
assert response["operation"] == "get_file"
assert response["account_id"] == "drive-test"
assert response["request"] == {"file_id": "fixture-drive-001"}
assert response["data"]["source"] == "offline-fixture"
```

### A4 — defaults remain deterministic

```python
response = DriveConnector(account_id="drive-test").list_files()

assert response["request"] == {
    "folder_id": None,
    "query": None,
    "limit": 20,
}
```

Repeated identical calls must produce equal envelopes. They must not create,
update, delete, or download anything.

### A5 — network access is forbidden

Run the A2 and A3 calls with socket creation patched to raise. Both calls must
still succeed and return `data.source == "offline-fixture"`. A test failure that
shows a socket, HTTP client, Drive SDK, authorization, or provider request is a
contract violation.

The repository's existing smoke coverage provides the baseline for these
invariants:

```bash
PYTHONPATH=harness/src pytest harness/tests/test_connectors.py harness/tests/test_offline.py
```

## Non-goals

This contract does not define Google Drive OAuth, refresh tokens, service
accounts, sharing permissions, provider query syntax, pagination semantics,
upload/update/delete behavior, or content retrieval. Those would require a
separate, explicitly authorized change and live-provider review.
