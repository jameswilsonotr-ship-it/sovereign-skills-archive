---
name: openspec-engineer
description: >
  Atomic OpenSpec engineering surface for proposing, validating, and auditing
  local change folders. Its offline pytest flashlight is read-only and
  default-deny for network access; use it when a change needs a deterministic
  local test pass or an audit trail without credentials.
version: 0.1.0
surfaces: [local]
---

# OpenSpec Engineer

This skill is the small, local engineering surface for an OpenSpec change. It
does not publish, call services, load credentials, or mutate the source tree.
The initial implementation is intentionally limited to an offline pytest
flashlight and an audit-log stub.

## Offline pytest flashlight

Run from this skill directory:

```bash
python scripts/flashlight.py path/to/tests --audit-log /tmp/openspec-audit.jsonl
```

The flashlight:

- disables pytest plugin autoloading;
- denies socket connections, DNS lookups, and URL-style network access by
  default;
- invokes pytest in-process without a shell;
- writes only the audit destination supplied by the caller;
- redacts common token, password, key, cookie, and bearer-token values before
  they reach an audit record.

`--allow-network` is an explicit escape hatch for a separately reviewed run;
it is never the default and is not appropriate for offline acceptance tests.

## Audit log stub

`scripts/audit_log.py` provides a dependency-free JSONL writer for lifecycle,
denial, completion, and error events. A caller can pass a file path or a
text stream. With no destination, events are returned to the caller but are
not persisted. This keeps the flashlight read-only unless `--audit-log` is
given.

The logger is an audit aid, not a security boundary. Do not put secrets in
test names, exception messages, or command-line arguments.

## Scope boundary

OpenSpec proposal/apply/archive orchestration is intentionally not implemented
here. A future change may add those operations behind the same offline and
audited contract.
