# GitHub Connector Contract

**OpenSpec change-id:** `second-salvo-17-github-contract`
**Slot:** S2-17
**Coverage:** included Ultra only

## Purpose

This document defines one bounded GitHub connector contract for the burn-wave
harness. It describes the offline, account-scoped call surface currently
implemented by `GithubConnector`; it is not a live GitHub API specification.

## Call envelope

Every connector call returns the same envelope:

```json
{
  "connector": "github",
  "operation": "<operation>",
  "account_id": "<logical account id>",
  "request": {},
  "data": {}
}
```

- `connector` is always `github`.
- `operation` identifies one operation from the allowlist below.
- `account_id` is required and identifies the selected account; it is not a
  credential.
- `request` contains the normalized operation arguments.
- `data` contains the provider-shaped result. In the harness it comes from the
  checked-in offline fixture.

`account_id` must be a non-empty string without surrounding whitespace and must
match `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`.

## Read surface

The connector exposes only these read operations:

| Operation | Required arguments | Optional arguments | Meaning |
| --- | --- | --- | --- |
| `search_repositories` | `query: string` | `limit: integer = 10` | Search repositories visible to the selected account |
| `get_issue` | `owner: string`, `repo: string`, `number: integer` | — | Read one issue |
| `list_pull_requests` | `owner: string`, `repo: string` | `state: string = "open"` | List pull requests for a repository |

Example request envelope:

```json
{
  "connector": "github",
  "operation": "search_repositories",
  "account_id": "github_unhex-ume",
  "request": {
    "query": "offline-harness",
    "limit": 2
  },
  "data": {
    "source": "offline-fixture"
  }
}
```

The operation names and argument shapes are the contract. The fixture payload
may remain small and deterministic; callers must not assume that it contains
fields beyond those supplied by the selected fixture or provider adapter.

## Read/write boundary

### Allowed

- Selecting a logical GitHub account with `account_id`.
- Reading repositories, issues, and pull-request listings through the three
  operations above.
- Returning deterministic fixture data for offline harness runs.

### Prohibited

This connector has no write authority. It must not create, update, or delete
repositories, branches, files, issues, pull requests, reviews, comments,
labels, hooks, releases, or other GitHub resources. It must not merge or close
pull requests, request reviews, or send notifications.

The cloud agent's own PR delivery is an agent workflow, not a connector
operation and not evidence that this connector has GitHub write access. Any
future live or write adapter requires a separate contract and change.

## Network and secret boundary

The harness implementation performs no network request and reads the local
`github` fixture. A runtime adapter must keep provider credentials outside the
call envelope, source them only from the host's secret mechanism, and never
persist or echo them in `request`, `data`, logs, fixtures, or documentation.
This document contains no secrets.

## Slot fences

This slot covers included Ultra only. OD, `CONV2_B`, and the Willow
`SKILL.md` surface are out of scope. Vultr and Cold Steel are distinct and
must not be treated as aliases or combined in this contract.

## Source of truth

- Implementation: `harness/src/sovereign_harness/connectors.py`
- Offline fixture: `harness/src/sovereign_harness/fixtures/github.json`
- Call-log corpus entry: `docs/burn-wave/corpora/MANIFEST.json`
