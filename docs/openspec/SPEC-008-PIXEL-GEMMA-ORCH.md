# SPEC-008 — Pixel Gemma Orchestration over Tailscale

**Status:** Draft  
**Base:** `skill-tree-intake`  
**Scope:** Specification only  
**Change class:** Atomic OpenSpec  

## Purpose

Define the contract for orchestrating Gemma inference on a Pixel-class Android
device while the control plane communicates with that device through a
Tailscale tailnet. The Pixel is the inference boundary: prompts and model
execution remain on the device unless a caller explicitly selects a separately
approved remote execution policy.

This specification does not select an Android framework, Gemma distribution,
quantization, Tailscale deployment mode, hosting provider, or persistence
technology. Those are implementation decisions that must satisfy these
requirements.

## Terms

| Term | Meaning |
|---|---|
| **Pixel** | The managed Android device that hosts the Gemma runtime and node adapter. |
| **Gemma runtime** | The local inference engine, model files, tokenizer, and runtime configuration on the Pixel. |
| **Orchestrator** | The trusted control-plane component that submits, tracks, cancels, and observes work. |
| **Node adapter** | The authenticated service boundary on the Pixel between Tailscale traffic and the Gemma runtime. |
| **Tailnet** | The private Tailscale network containing the orchestrator and eligible Pixel nodes. |
| **Job** | One bounded inference request with an identity, policy, deadline, and lifecycle. |
| **Local-only** | A policy in which prompt content, model execution, and generated output stay on the Pixel and trusted tailnet components. |

## Atomic requirement groups

### PG-001 — Explicit system boundary

**Requirement:** The system SHALL model the orchestrator, tailnet, Pixel node
adapter, Gemma runtime, model artifacts, and caller as separate trust and
failure boundaries. A deployment SHALL document which component owns each
boundary before it is admitted.

**Scenario:** An operator reviews a deployment. The documentation identifies
the orchestrator endpoint, the authorized Pixel node, the node adapter, the
runtime process, and the model artifact location without relying on implicit
hostnames or undocumented process relationships.

**Acceptance:** A topology record names every boundary, its owner, its
communication direction, and its failure behavior. A missing or ambiguous
boundary blocks readiness.

### PG-002 — Tailnet-only transport

**Requirement:** The node adapter SHALL accept orchestration traffic only over
the approved Tailscale interface or an equivalent tailnet-scoped path. The
service SHALL NOT require a publicly routable listener, port-forward, or
Tailscale Funnel exposure.

**Scenario:** A client attempts to reach the adapter from outside the tailnet.
The request is not accepted, while an authorized orchestrator on the tailnet
can connect to the same logical service.

**Acceptance:** Network inspection shows no required public ingress. The
adapter rejects traffic that does not arrive through the approved private
network boundary.

### PG-003 — Identity and authorization

**Requirement:** Every request SHALL be attributable to both an orchestrator
identity and a Pixel node identity. Tailscale device identity and ACL policy
SHALL establish network reachability; an application-level authorization check
SHALL still enforce the allowed operation, node, and policy.

**Scenario:** A tailnet member can reach the adapter but is not authorized to
submit inference jobs. The adapter denies the submission and does not invoke
Gemma.

**Acceptance:** Authorization is evaluated before prompt processing. Denial
responses do not disclose model state, prompt content, or secret material.

### PG-004 — Secret-free specification and operation

**Requirement:** Source, logs, job metadata, examples, and documentation SHALL
NOT contain private keys, auth keys, bearer tokens, passwords, recovery codes,
or copied device credentials. Runtime credentials SHALL be injected through
the deployment's approved secret mechanism and SHALL never be returned in an
API response.

**Scenario:** An operator exports a job record or diagnostic bundle. It
contains identifiers and redacted metadata, but no credential value or
credential-shaped payload.

**Acceptance:** Secret scanning passes for the repository and generated
diagnostics. Configuration validation rejects inline credential values where
the deployment contract requires references to an external secret store.

### PG-005 — Capability-checked node registration

**Requirement:** A Pixel node SHALL register with a non-secret node identifier,
software and runtime versions, model identifier, supported input/output
limits, power and thermal state, and current availability. Registration SHALL
not make the node eligible until all required capability fields are validated.

**Scenario:** A node advertises a context limit smaller than the requested
policy. The orchestrator excludes it from scheduling rather than discovering
the mismatch after inference begins.

**Acceptance:** Registration is rejected for missing, stale, contradictory, or
over-limit capabilities. Capability data is treated as advisory until the
node's readiness check succeeds.

### PG-006 — Versioned job contract

**Requirement:** The adapter SHALL expose a versioned job contract containing a
unique job ID or caller-supplied idempotency key, model selector, input
messages, generation limits, policy, deadline, and cancellation behavior.
Unknown required fields or unsupported contract versions SHALL fail closed.

**Scenario:** The orchestrator submits a job using a supported contract
version. The adapter validates the complete request and returns an accepted
job identity before inference starts.

**Acceptance:** Contract validation produces stable, machine-readable errors.
The contract defines maximum prompt size, maximum output budget, deadline
format, and permitted model selectors without embedding implementation
secrets.

### PG-007 — Local-only execution policy

**Requirement:** Local-only SHALL be the default execution policy. Under that
policy, prompt content and generated output SHALL be processed by the Gemma
runtime on the Pixel and may traverse only authorized tailnet components.
There SHALL be no implicit cloud fallback, third-party telemetry upload, or
remote model substitution.

**Scenario:** The Pixel loses access to the orchestrator or an optional remote
service while a local-only job is eligible. The job fails or waits according
to policy; its content is not rerouted to another provider.

**Acceptance:** A policy test demonstrates that local-only jobs invoke only the
declared Pixel runtime. Any non-local execution mode requires an explicit
request policy and separate authorization.

### PG-008 — Model and runtime pinning

**Requirement:** Each job SHALL resolve to an approved Gemma model identifier,
artifact digest or equivalent immutable version, tokenizer version, runtime
version, and execution profile. A node SHALL reject a job when the resolved
artifacts do not match its admitted capability record.

**Scenario:** The model file is replaced while the node is registered. New
jobs are held or rejected until capability registration and readiness are
re-established for the new artifact.

**Acceptance:** Every completed result records the resolved model and runtime
identity. A mutable alias alone is insufficient for reproducible execution.

### PG-009 — Admission control and resource budgets

**Requirement:** The node adapter SHALL perform admission checks before placing a
job in the runtime queue. Checks SHALL include input and output budgets,
deadline feasibility, queue capacity, memory headroom, thermal state, battery
policy, and model availability.

**Scenario:** A job would exceed the configured output budget or available
memory. The adapter rejects it before loading or invoking the model and
returns the violated budget category.

**Acceptance:** No admitted job can exceed the declared per-job budgets.
Admission decisions are observable without recording prompt content.

### PG-010 — Deterministic scheduling and concurrency limits

**Requirement:** The orchestrator and node adapter SHALL define an explicit
queue ordering and concurrency limit for each Pixel/model profile. Scheduling
SHALL honor priority only within authorized bounds and SHALL prevent starvation
of bounded-priority work.

**Scenario:** Multiple jobs arrive while the Pixel is busy. The adapter
accepts only work within capacity, preserves the documented ordering, and
reports queue position or an equivalent state without promising an exact start
time.

**Acceptance:** Queue capacity, active-job capacity, priority range, and
fairness behavior are configuration-visible and tested under saturation.

### PG-011 — Lifecycle, idempotency, and cancellation

**Requirement:** A job SHALL have a monotonic lifecycle with at least
`accepted`, `queued`, `running`, and one terminal state. Repeating a submission
with the same idempotency key SHALL not create duplicate inference work.
Cancellation SHALL be best effort, authenticated, and terminally observable.

**Scenario:** The orchestrator retries after a transport interruption. The
adapter returns the existing job state for the idempotency key. If cancellation
arrives during generation, the runtime stops at its next supported boundary
and the result is marked cancelled or partially unavailable.

**Acceptance:** State transitions are valid and monotonic. A terminal job is
never silently re-run by a retry.

### PG-012 — Deadline, timeout, and retry semantics

**Requirement:** Jobs SHALL carry an absolute deadline or an equivalent
bounded timeout. The system SHALL distinguish connection timeout, queue
timeout, runtime timeout, and caller cancellation. Retries SHALL be limited,
backoff-controlled, and safe only when the idempotency contract prevents
duplicate execution.

**Scenario:** The tailnet connection drops after the Pixel begins inference.
The orchestrator reconnects and queries the existing job rather than blindly
submitting a second job.

**Acceptance:** Each timeout category has a stable error code and terminal
behavior. No retry policy can extend a job beyond its caller-visible deadline.

### PG-013 — Result, error, and provenance contract

**Requirement:** A terminal response SHALL include the job identity, terminal
state, model/runtime provenance, timing measurements, usage counts where
available, and either a generated result or a structured error. Errors SHALL
identify retryability without exposing internal paths, credentials, or prompt
content.

**Scenario:** Gemma produces a result. The orchestrator receives the text or
structured output together with finish reason, token or byte accounting when
available, and the immutable model/runtime identity used.

**Acceptance:** Consumers can distinguish success, cancellation, validation
failure, capacity rejection, runtime failure, deadline expiry, and transport
failure without parsing human prose.

### PG-014 — Streaming and bounded delivery

**Requirement:** If streaming is supported, chunks SHALL be ordered,
associated with one job, bounded in size, and terminated by an authenticated
terminal event. If a stream disconnects, the final job state SHALL remain
queryable. The adapter SHALL apply backpressure and SHALL not buffer
unbounded output.

**Scenario:** A caller stops reading a stream. The adapter applies the
documented backpressure behavior, cancels or pauses according to policy, and
retains only bounded state needed for final reconciliation.

**Acceptance:** A disconnected stream cannot cause unbounded memory growth.
The non-streaming result query remains authoritative for completion.

### PG-015 — Health, readiness, and thermal safety

**Requirement:** The Pixel SHALL expose separate liveness, readiness, and
capacity signals. Readiness SHALL require a healthy adapter, reachable model
artifacts, compatible runtime, sufficient resources, and an acceptable thermal
and power state. Thermal or battery protection SHALL stop new admissions before
unsafe operation.

**Scenario:** The Pixel enters a thermal throttling state. Liveness remains
available for status and cancellation, but readiness becomes false and new
inference jobs are rejected or deferred.

**Acceptance:** Health checks never claim inference readiness solely because
the network process is alive. Recovery requires the readiness conditions to
become true again.

### PG-016 — Privacy, retention, and redaction

**Requirement:** Prompt, context, and output data SHALL be classified as
content data and SHALL be excluded from ordinary logs, metrics, traces,
registration records, and health responses. Retention of content, if enabled,
SHALL be explicit, bounded, encrypted at rest, access-controlled, and
deletable.

**Scenario:** An inference fails. Diagnostics contain the job ID, error class,
timings, and redacted model metadata, but not the prompt, generated text, or
raw request headers.

**Acceptance:** Automated tests verify redaction on success, failure, retry,
timeout, cancellation, and crash-recovery paths. Default retention for
content is zero unless an approved policy says otherwise.

### PG-017 — Observability without content leakage

**Requirement:** The system SHALL emit metrics and structured events for
admission, queueing, execution, completion, cancellation, rejection,
resource state, and transport health. Telemetry SHALL use stable non-content
identifiers, bounded cardinality, and redaction rules consistent with
PG-016.

**Scenario:** Operators investigate elevated latency. They can compare queue
wait, model execution, transport, thermal, and failure metrics by node and
model version without retrieving user prompts or outputs.

**Acceptance:** Every terminal job is represented by sufficient non-content
telemetry to diagnose its class of outcome. Telemetry failure does not block
or silently alter local-only inference.

### PG-018 — Failure isolation and recovery

**Requirement:** Failure of the orchestrator, tailnet path, node adapter, model
runtime, or Pixel power state SHALL be isolated and represented by an
explicit recovery state. The system SHALL not report success until the
authoritative result is durably available to the caller or acknowledged by
the defined delivery contract.

**Scenario:** The runtime crashes during generation. The adapter marks the job
as runtime-failed or unknown according to its recovery evidence, restarts only
within the configured policy, and does not fabricate or replay a result.

**Acceptance:** Restart and network-partition tests produce no false success,
duplicate terminal delivery, or orphaned job that cannot be reconciled.

### PG-019 — Controlled rollout and rollback

**Requirement:** Model artifacts, runtime versions, adapter versions, and
policy changes SHALL be staged, health-checked, and attributable before
serving production jobs. Rollback SHALL restore the last admitted compatible
combination without invalidating the provenance of already completed jobs.

**Scenario:** A new Gemma artifact passes installation but fails readiness or
quality gates. The node remains on the prior admitted combination and no
traffic is routed to the failed candidate.

**Acceptance:** Rollout records identify candidate, approver, checks, and
outcome without containing secrets. A failed rollout leaves the node either
serving the prior version or explicitly unavailable.

### PG-020 — Conformance and operational acceptance

**Requirement:** An implementation SHALL pass conformance tests covering
network isolation, authorization, secret absence, capability registration,
contract validation, local-only routing, admission, lifecycle and
idempotency, deadlines, streaming bounds, thermal protection, privacy
redaction, recovery, and rollback before it is declared operational.

**Scenario:** An operator runs the acceptance suite against a fresh Pixel
registration and an authorized orchestrator. The suite reports each PG gate
independently and stops release approval when any mandatory gate fails.

**Acceptance:** The release record links each of PG-001 through PG-020 to
evidence, test result, implementation version, model/runtime provenance, and
operator or automation identity. Passing the suite does not authorize
deployment outside the approved tailnet or execution policy.

## Non-goals

- Selecting a specific Gemma checkpoint, quantization, Android inference
  engine, or Pixel hardware generation.
- Implementing the adapter, orchestrator, Android application, or CI pipeline.
- Publishing a public API or exposing the Pixel through Tailscale Funnel.
- Making safety, legal, medical, financial, or other high-impact decisions
  from model output without a separate reviewed policy.
- Treating Tailscale connectivity as a substitute for application
  authorization, input validation, privacy controls, or auditability.
