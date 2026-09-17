# Vesper MCP capacity bind stub

Status: **non-live protocol stub**
Related contract: [SPARK_BIND](../SPARK_BIND.md) ·
[SPEC-001](../SPARK_BIND.md#spec-001-alignment) ·
[BASIC_TIER](../SPARK_BIND.md#basic_tier-alignment)

## Purpose

Define a small, transport-neutral handshake for advertising Vesper capacity
before the Spark bridge schedules work. This does not identify a live
endpoint, select a transport, or provide authentication material.

## Bind request

```json
{
  "schema": "vesper-mcp-bind/v0",
  "request_id": "REQ_PLACEHOLDER",
  "client": "spark-bridge",
  "requested_operations": ["spark.send"],
  "requested_profile": "BASIC_TIER",
  "requested_in_flight": 1
}
```

## Bind response

```json
{
  "schema": "vesper-mcp-bind/v0",
  "request_id": "REQ_PLACEHOLDER",
  "status": "bound",
  "server": "vesper",
  "capacity": {
    "profile": "BASIC_TIER",
    "max_in_flight": 1,
    "burst": 1,
    "sustained_per_minute": "DECLARED_BY_VESPER",
    "queue_timeout_seconds": "DECLARED_BY_VESPER",
    "request_timeout_seconds": "DECLARED_BY_VESPER"
  },
  "operations": ["spark.send"],
  "backpressure": "reject",
  "receipt_mode": "secret_free"
}
```

The values marked `DECLARED_BY_VESPER` are placeholders. The caller must
honor the returned values and must not substitute guessed limits.

## Capacity notes

- Vesper is authoritative for `max_in_flight`, burst, rate, and timeout
  values.
- The BASIC_TIER default is one in-flight operation until Vesper advertises a
  different safe limit.
- A caller must reserve capacity before starting a send and release it after
  a terminal result.
- A response of `busy`, `degraded`, or `unavailable` must not be converted
  into an automatic retry loop.
- A timeout after dispatch is not proof of failure; surface the operation as
  `unknown` and reconcile through the bind's receipt mechanism.
- Unsupported operations must fail closed with `operation_not_supported`.
- Capacity is scoped to the bound session and must not be treated as a global
  account quota.

## State sketch

```text
unbound
  └─ bind ──> bound
                ├─ reserve ──> in_flight ──> terminal ──> released
                ├─ busy/degraded ──> backoff_required
                └─ unavailable ──> unbound
```

The bridge owns scheduling. Vesper owns the declaration and may reduce
capacity between binds. The bridge must stop dispatching when the declaration
expires or the transport reports that the bind is no longer valid.

## Transport TODOs

- [ ] Choose stdio or Streamable HTTP for the first Vesper implementation.
- [ ] Define the bind lifetime and renewal behavior.
- [ ] Define the receipt lookup needed to reconcile `unknown`.
- [ ] Define the exact MCP error mapping for `busy`, `degraded`, and
      `operation_not_supported`.
- [ ] Add a live, secret-free contract fixture once the endpoint exists.

Until those items are complete, this file remains a design stub and should
not be used to configure a production MCP client.
