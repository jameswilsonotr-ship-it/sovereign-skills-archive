# Spark Bind

Status: **draft stub — not a live integration**  
Owner: Sovereign Skills Archive  
Surface: Gemini Spark web + Vesper MCP

This document defines the boundary between the Gemini Spark web surface and
Vesper's MCP-capacity handshake. It records the intended contract without
claiming that web automation, Gmail delivery, or an MCP endpoint is currently
connected.

## Scope

- Provide a safe stub for sending from the Gemini Spark web UI.
- Make the delivery action explicit: click Spark's real **Send** control.
- Keep Gmail drafts out of the delivery path.
- Define a small, capacity-aware bind envelope for Vesper.
- Leave credentials, cookies, tokens, endpoint URLs, and personal addresses
  outside this repository.

## Stubs

- [Gemini Spark web Send automation](stubs/GEMINI_SPARK_SEND.md)
- [Vesper MCP capacity bind](stubs/VESPER_MCP_BIND.md)

Both stubs are design notes. They are not executable automation and do not
imply that a browser session or MCP server is available.

## Delivery invariant

The automation must:

1. Attach to an already authenticated Spark browser session or require an
   operator-approved login flow. It must never accept or store credentials.
2. Open the Spark compose surface and populate the intended recipient,
   subject, and body.
3. Verify that it is on the Spark web surface, not Gmail.
4. Require an explicit send decision.
5. Click the visible Spark **Send** button.
6. Wait for a Spark sent/confirmation state and record only a
   secret-free result.

Saving a Gmail draft is not success. A Gmail draft may be used only as an
explicitly separate preparation step and must never be reported as delivery.

## Capacity bind invariant

Vesper owns the capacity declaration. A caller must not infer capacity from a
successful connection or silently exceed the declared limit. The bind should
negotiate:

- protocol and transport;
- maximum in-flight operations;
- burst and sustained rate limits;
- request and queue timeouts;
- supported operation names;
- backpressure behavior; and
- a degraded or unavailable state.

The bind envelope is intentionally abstract until the canonical MCP endpoint
and Vesper runtime are selected. See the [Vesper MCP capacity stub](stubs/VESPER_MCP_BIND.md).

## SPEC-001 alignment

This bridge follows the **SPEC-001** contract boundary:

- delivery is an observable action, not a draft-side effect;
- every side effect has an explicit confirmation point;
- receipts are secret-free and identify outcome, not private session data;
- unavailable or unverified capabilities remain marked as stubs.

The canonical SPEC-001 file is not present in this archive yet. Until it is
added, this section is the local cross-link for the bridge contract:
[SPEC-001](#spec-001-alignment).

## BASIC_TIER alignment

The **BASIC_TIER** profile is the conservative implementation target:

- one operator-approved send at a time;
- no background listener;
- no credential handling;
- no automatic retries after an uncertain send result;
- one bounded MCP request in flight unless Vesper advertises more;
- a human-readable, secret-free receipt for each attempted action.

The canonical BASIC_TIER file is not present in this archive yet. Until it is
added, this section is the local cross-link for the tier boundary:
[BASIC_TIER](#basic_tier-alignment).

## Secret boundary

Do not commit or paste any of the following:

- API keys, OAuth tokens, cookies, session exports, or refresh tokens;
- real recipient addresses or message bodies;
- browser profile paths that expose private state;
- private MCP URLs, hostnames, or bearer headers;
- screenshots containing account data.

Use placeholders such as `SPARK_SESSION`, `MCP_ENDPOINT`, and
`RECIPIENT_PLACEHOLDER` in future examples. Keep live configuration in the
operator's secret store or local environment, never in this archive.

## Acceptance checklist

- [ ] The implementation targets Gemini Spark's compose UI.
- [ ] The implementation clicks the real Spark **Send** control.
- [ ] Gmail draft creation is not counted as delivery.
- [ ] An uncertain post-click state is surfaced for operator review.
- [ ] Vesper capacity is read from the bind response and enforced.
- [ ] Backpressure and unavailable states are explicit.
- [ ] No secret or personal content appears in logs, fixtures, or receipts.
- [ ] SPEC-001 and BASIC_TIER canonical paths are added when those contracts
      land in the archive.
