# meter-watch

## Purpose

Observability contract for Cursor Ultra meter scrape, desk reporting, and CinC
wake thresholds. No spend actions.

Gage Burn owns the live scrape. Applying or reviewing this contract MUST NOT
open the Cursor Spending UI or perform a live scrape.

## Requirements

### Requirement: Scrape floor and source

The meter watcher SHALL enforce a floor of at least 5 minutes between
successive scrapes and SHALL prefer `https://www.cursor.com/dashboard`
Spending. Settings/usage endpoints that return 404 or empty results MUST NOT
be treated as authoritative.

#### Scenario: Floor interval respected

- **WHEN** the meter watcher runs continuously
- **THEN** successive scrapes MUST be spaced >= 5 minutes apart

#### Scenario: Dashboard Spending preferred

- **WHEN** settings/usage returns 404 or empty
- **THEN** the watcher MUST use dashboard Spending and MUST NOT invent usage
  figures

#### Scenario: Live scrape ownership

- **WHEN** this contract is applied or reviewed
- **THEN** the task MUST NOT open the Spending UI; Gage Burn remains the owner
  of live scrape execution

### Requirement: Report channels and timestamps

The meter watcher SHALL report Ultra, Models, Other, and On-Demand fields to
Meter Burn Desk (`5a6dff2d-8383-470f-952d-97b50ef2e819`) and MAY flag climbs
on Burn Spot Line (`86c6162b`) via Ember Spot. Every report MUST include the
scrape timestamp in CT.

#### Scenario: Desk report after scrape

- **WHEN** a scrape completes with Ultra / Models / Other / On-Demand fields
- **THEN** a report MUST be posted to Meter Burn Desk with those fields and
  scrape time (CT)

### Requirement: CinC wake thresholds

The meter watcher SHALL wake Bunny / Burn Flip Swarm only when included usage
is >= 80%, On-Demand is climbing further past OVER, or a billing reset is
detected. It SHALL report observations without waking when none of those
conditions is met.

#### Scenario: Wake at included >= 80%

- **WHEN** Cursor Models (included) scrape shows >= ~80%
- **THEN** the watcher MUST wake Bunny / Burn Flip Swarm and MUST NOT initiate
  spend actions

#### Scenario: Wake when On-Demand climbs further past OVER

- **WHEN** On-Demand increases further beyond an already OVER state
- **THEN** the watcher MUST wake Bunny / Burn Flip Swarm and MUST NOT
  recommend or execute additional On-Demand spend

#### Scenario: Wake on reset

- **WHEN** a billing reset is detected
- **THEN** the watcher MUST wake Bunny / Burn Flip Swarm and MUST NOT initiate
  spend actions

#### Scenario: OD already OVER — no spend

- **WHEN** On-Demand is already OVER (for example, $14.25/$14)
- **THEN** the watcher MUST note OVER status, MUST NOT treat OVER alone as a
  wake threshold, and MUST NOT recommend or execute additional On-Demand spend

### Requirement: Observability only

The meter-watch capability MUST NOT perform purchase, upgrade, or spend
mutations and MUST NOT invoke a billing mutation API or UI purchase path.

#### Scenario: No spend side effects

- **WHEN** any meter-watch task runs
- **THEN** no billing mutation API or UI purchase path SHALL be invoked
