# T3-22 Included Ultra eligibility

## ADDED Requirements

### Requirement: T3-22 allows only Included Ultra

The evaluator MUST return `ALLOW` only when the request has slot `T3-22`,
entitlement `INCLUDED`, and tier `Ultra` as exact string values.

#### Scenario: exact Included Ultra request is allowed

- **GIVEN** a request with slot `T3-22`, entitlement `INCLUDED`, and tier
  `Ultra`
- **WHEN** the request is evaluated
- **THEN** the decision is `ALLOW`
- **AND** the fallback is `null`

#### Scenario: Included non-Ultra request is denied

- **GIVEN** a request with slot `T3-22`, entitlement `INCLUDED`, and a tier
  other than `Ultra`
- **WHEN** the request is evaluated
- **THEN** the decision is `DENY`
- **AND** the reason codes include `TIER_NOT_ULTRA`

### Requirement: On-Demand is never eligible

The evaluator MUST return `DENY` for every On-Demand request, including an
On-Demand request whose tier is `Ultra`.

#### Scenario: On-Demand Ultra request is denied

- **GIVEN** a request with slot `T3-22`, entitlement `ON_DEMAND`, and tier
  `Ultra`
- **WHEN** the request is evaluated
- **THEN** the decision is `DENY`
- **AND** the reason codes include `ON_DEMAND_NOT_ALLOWED`
- **AND** the fallback is `null`

#### Scenario: On-Demand non-Ultra request is denied without rerouting

- **GIVEN** a request with slot `T3-22`, entitlement `ON_DEMAND`, and a tier
  other than `Ultra`
- **WHEN** the request is evaluated
- **THEN** the decision is `DENY`
- **AND** the result contains no reroute target

### Requirement: malformed requests fail closed

The evaluator MUST return `DENY` for missing, malformed, or non-matching
request fields. A denial MUST include at least one stable reason code and a
null fallback.

#### Scenario: missing entitlement is denied

- **GIVEN** a request without an entitlement
- **WHEN** the request is evaluated
- **THEN** the decision is `DENY`
- **AND** the reason codes include `ENTITLEMENT_NOT_INCLUDED`

#### Scenario: wrong slot is denied

- **GIVEN** a request with a slot other than `T3-22`
- **WHEN** the request is evaluated
- **THEN** the decision is `DENY`
- **AND** the reason codes include `INVALID_REQUEST`
