---
id: second-salvo-19-gmail-contract
title: Gmail connector contract
status: proposed
slot: S2-19
profile: included Ultra
---

# Gmail connector contract

This is the contract for the **included Ultra** Gmail connector surface in
OpenSpec change `second-salvo-19-gmail-contract` (slot **S2-19**). It is a
documentation-only, read-only contract. It does not claim that a Gmail
account, credential, mailbox, or connector is available.

## Scope and hard boundary

The connector may expose bounded, read-only thread search against an
operator-approved Gmail account when a future implementation supplies its own
authenticated runtime. This document defines the interface and the
secret-free receipt; it does not authorize access to mail.

Included:

- the `included Ultra` profile only;
- the `search_threads` operation;
- bounded result metadata and normalized error categories;
- redaction before logging, persistence, telemetry, or display.

Excluded:

- sending, drafting, replying, forwarding, labeling, deleting, or changing
  mail;
- attachment or message-body retrieval;
- background mailbox listeners or automatic retries;
- credentials, OAuth flows, cookies, tokens, personal addresses, or live
  mailbox data;
- deployment, hosting, infrastructure, and unrelated S2 slots.

The contract is not a live Gmail test plan. Verification uses static checks
and offline synthetic inputs only; no Gmail API, browser session, or live
mailbox may be contacted.

## Contract version and operation

Contract version: `gmail-read-v1`.

The only supported operation is:

```text
search_threads(request) -> result
```

The connector MUST reject any operation not in this allowlist. A caller MUST
provide an opaque `account_ref` that identifies an approved runtime account;
the value MUST NOT be an email address or credential.

### Request

```json
{
  "operation": "search_threads",
  "account_ref": "ACCOUNT_REF",
  "query": "QUERY_PLACEHOLDER",
  "limit": 20,
  "page_token": "PAGE_TOKEN_PLACEHOLDER"
}
```

Request rules:

- `query` is supplied at runtime and MUST be treated as sensitive input. It
  MUST NOT appear in a receipt, log, trace, metric label, or exception.
- `limit` MUST be an integer from 1 through 50; a missing value defaults to 20.
- `page_token` is optional, opaque, and runtime-only. It MUST NOT be logged,
  persisted, or returned in diagnostics.
- The connector MUST reject malformed requests before any provider call.
- The connector MUST NOT accept credentials or provider-specific headers in
  the request contract.

### Success result

The public result is metadata-only:

```json
{
  "status": "ok",
  "operation": "search_threads",
  "account_ref": "ACCOUNT_REF",
  "result_count": 0,
  "has_next_page": false,
  "threads": []
}
```

Each returned thread record, when present, is limited to:

```json
{
  "thread_ref": "THREAD_REF",
  "message_count": 0,
  "received_at_bucket": "YYYY-MM-DD"
}
```

`thread_ref` MUST be an opaque redacted reference, never a raw provider ID.
`received_at_bucket` MUST be the coarsest time precision needed by the
consumer; exact timestamps are not part of this contract. Message content,
addresses, subjects, snippets, labels, headers, links, attachment metadata,
and provider payloads are not result fields.

The connector MUST bound `result_count` and the number of `threads` entries by
the requested `limit`. It MUST discard an unrecognized provider field rather
than pass it through.

### Failure result

Failures use a stable category and no provider payload:

```json
{
  "status": "error",
  "operation": "search_threads",
  "error_category": "rate_limited",
  "retry_after_bucket": "RETRY_AFTER_BUCKET"
}
```

Allowed `error_category` values are:

| Category | Meaning |
| --- | --- |
| `invalid_request` | The request failed local validation. |
| `auth_required` | The approved runtime has no usable authorization. |
| `permission_denied` | The runtime is not allowed to perform the operation. |
| `rate_limited` | The provider requested backoff. |
| `provider_unavailable` | The provider could not complete the call. |
| `redaction_failed` | Safe normalization could not be completed. |
| `unsupported_operation` | The operation is outside this contract. |

Raw provider status text, response bodies, request URLs, headers, tokens, and
stack traces MUST never cross the connector boundary. `retry_after_bucket` is
optional and coarse; an exact provider value is runtime-only.

## Redaction expectations

Redaction is a boundary, not a presentation feature. The connector MUST
normalize and redact in memory before emitting any receipt or diagnostic. The
default action for an unknown field is **drop**, not mask-and-forward.

| Data | Contract treatment |
| --- | --- |
| OAuth access/refresh tokens, API keys, cookies, authorization headers | Never accept, store, log, or return |
| Email addresses and account identities | Replace with `ACCOUNT_REF`; never emit the source value |
| Gmail message/thread IDs | Replace with opaque `THREAD_REF`; never emit the source value |
| Query text, subjects, snippets, bodies, headers, labels | Drop entirely |
| Attachments, MIME data, URLs, and provider payloads | Drop entirely |
| Exact timestamps and provider retry values | Bucket or drop |
| Provider errors and stack traces | Map to `error_category`; drop source text |
| Unknown fields | Drop and increment an internal non-content counter only |

If correlation is required, an implementation may derive a short-lived,
one-way opaque reference in memory. The derivation key and source identifier
MUST remain outside logs, fixtures, receipts, and repository content. A
redaction failure is a hard stop: return `redaction_failed`, emit no partial
payload, and do not retry automatically.

## Secret-free receipt

An implementation may produce one receipt per attempted operation with only
these fields:

```json
{
  "receipt_version": "1",
  "receipt_id": "RECEIPT_ID",
  "operation": "search_threads",
  "status": "ok",
  "result_count": 0,
  "latency_bucket": "LT_1S",
  "recorded_at": "UTC_TIMESTAMP"
}
```

`receipt_id` is locally generated and opaque. `recorded_at` is UTC and may be
rounded to the precision required for operations. The receipt MUST omit
`account_ref`, query text, page tokens, thread references, addresses, content,
provider IDs, and all authentication material unless a downstream review
explicitly approves a separately redacted field. The default receipt above
contains no mailbox content.

## Operational behavior

- One request is one bounded `search_threads` attempt.
- The connector MUST enforce a caller-provided timeout and MUST not retry an
  uncertain provider result automatically.
- Rate limiting and unavailability are reported through the failure categories
  above; they are not hidden as an empty search result.
- Logs and metrics may include operation, status, error category, bounded
  count, and coarse latency only.
- A disabled or unavailable connector remains unavailable; this contract does
  not authorize fallback to another mail surface.

## Offline verification

Verification for this change is limited to:

1. Markdown and JSON examples contain placeholders only.
2. Static review confirms the operation allowlist, field bounds, and redaction
   rules.
3. An offline synthetic `search_threads` input produces metadata-only output.
4. A fixture containing credentials, addresses, content, provider IDs, or
   unknown fields produces no such values in the receipt or diagnostic.
5. No test opens a network connection, invokes Gmail, uses a browser session,
   or reads live mail.

Acceptance checklist:

- [ ] The contract is limited to the included Ultra profile.
- [ ] Only read-only `search_threads` is supported.
- [ ] Provider payloads and sensitive request fields are excluded from output.
- [ ] Unknown fields default to drop.
- [ ] Redaction failure emits no partial payload.
- [ ] Verification remains offline and synthetic.
- [ ] No credentials, secrets, personal addresses, or unredacted mail content
      are committed.
