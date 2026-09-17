# vultr-gateway

## Purpose

Paper and stub for Vultr `vc2-1c-2gb` ORD headless coding gateway: Docker + Letta + Ollama, Tailscale-only ingress. Vultr is cloud gateway under Iron Pearl BASIC — **not** Cold Steel.

## Requirements

### Requirement: Instance paper target

The gateway spec SHALL target Vultr plan `vc2-1c-2gb` in ORD labeled `mcp-vultr` and MUST mark live provision as requiring Bunny YES (Olette asks).

#### Scenario: Provision gated

- **WHEN** apply reaches a live Vultr create/resize/destroy, API, or spend step
- **THEN** the step MUST halt pending Bunny YES and MUST NOT invent IP addresses or API keys

### Requirement: Stack composition

The headless gateway SHALL run Docker with Letta and Ollama as the coding runtime stack.

#### Scenario: Stack declared

- **WHEN** the gateway stub is documented or scaffolded
- **THEN** Docker + Letta + Ollama MUST be named as required components

### Requirement: Tailscale-only ingress

Ingress to the gateway MUST be Tailscale-only; public SSH/HTTP exposure SHALL NOT be the default.

#### Scenario: No public default

- **WHEN** gateway networking is specified
- **THEN** Tailscale MUST be the sole documented ingress path for coding control

### Requirement: Not Cold Steel

Vultr gateway work MUST NOT include bare-metal Cold Steel edge tasks (GMKtec K15, Jetson Orin Nano, HP EliteDesk Ashtabula).

#### Scenario: Steel excluded

- **WHEN** this capability is applied
- **THEN** no bare-metal Steel provision or offline-CLI edge work SHALL be included in the change scope
