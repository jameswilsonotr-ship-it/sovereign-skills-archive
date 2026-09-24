# OpenSpec module catalog

This directory contains proposed contracts for the sovereign connector and
runtime surfaces. [`BASIC_TIER.md`](./BASIC_TIER.md) is the shared minimum
contract; every module spec links back to it and must satisfy its checklist
before implementation.

## Modules

| Module | Boundary |
|---|---|
| [`drive_connector`](./modules/drive_connector.md) | Drive artifact staging, retrieval, and receipts |
| [`github_connector`](./modules/github_connector.md) | Scoped repository reads and reviewable commits |
| [`linear_connector`](./modules/linear_connector.md) | Team-scoped issue discovery and updates |
| [`gmail_connector(account_id)`](./modules/gmail_connector.md) | Account-scoped email control-plane transport |
| [`phone_mcp_termux`](./modules/phone_mcp_termux.md) | Device-bound Termux MCP capabilities |
| [`vultr_letta_runtime`](./modules/vultr_letta_runtime.md) | Hosted Letta-compatible sessions and memory tiers |
| [`spark_escalation`](./modules/spark_escalation.md) | Bounded light-to-heavy task handoff |

## Lifecycle

These are specifications, not claims that the integrations are implemented.
Implementation should proceed from read-only and dry-run paths, then add
approved writes with receipts. Any change to `BASIC_TIER` requires reviewing
all module specs in the same change.
