---
id: api-rate-limits
title: API rate limits
status: proposed
owner: platform
priority: high
summary: Add predictable per-client request limits to the public API.
tags:
  - api
  - reliability
dependencies: auth-service
---

# API rate limits

## Requirements

- Clients receive a `429` response after exceeding their configured limit.
- Responses include a `Retry-After` header.

## Acceptance

- [ ] A client at the limit receives `429`.
- [ ] The response contains `Retry-After`.
