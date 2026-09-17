# Basic-tier implementation tasks

This checklist turns the Basic specification into an auditable, staged
implementation. Tasks that touch paid infrastructure, phone capabilities, or
Gemini require an operator decision and are not implied by this docs-only
change.

## 1. Contract and repository hygiene

- [ ] Review `proposal.md`, `spec.md`, and `design.md` as one contract.
- [ ] Confirm PRs #5–#10 are cited as source/design evidence, not as proof that
      a service is live.
- [ ] Keep the change under `specs/openspec/basic/`.
- [ ] Run `git diff --check`.
- [ ] Run a repository scan for credentials, private keys, model weights,
      APK/AAB files, native binaries, and unredacted private content.
- [ ] Confirm no large Drive artifact was unpacked and `CONV2_B` was not
      opened, reconstructed, or copied.
- [ ] Confirm no Ansible file or execution path is introduced.
- [ ] Confirm no CMV identity, CMV Gmail path, or CMV fallback is introduced.

## 2. Offline contract harness

- [ ] Add fixture validation for the phone health response:
      `runner`, `model_id`, `device_id`, and `ready`.
- [ ] Test ready, unavailable, malformed, and timeout health states.
- [ ] Test that the phone fixture accepts only `GET /health`.
- [ ] Test router decisions for:
      local admission, approved Vultr, explicit Spark, deferred, and refused.
- [ ] Test that Letta failure degrades to stateless Vultr or a clear error.
- [ ] Test that Gemini failure returns Tier C unavailable and never changes to
      CMV.
- [ ] Make the harness fully offline; no real phone, SMS, camera, Gemini, or
      Vultr call may be required.

## 3. Tailscale admission

- [ ] Define deployment-only Tailscale tags, node identities, and ACL rules.
- [ ] Bind phone `:8081/health` to localhost or the phone's `100.x` address.
- [ ] Bind the Vultr gateway to its `100.x` address and deny public access.
- [ ] Allow the router only the phone health path and required Vultr paths.
- [ ] Add application authentication where the selected service supports it.
- [ ] Verify the phone and Vultr public interfaces cannot serve these ports.
- [ ] Pin the Olette-box SSH host key before any SFTP test.
- [ ] Record ACL revision and tested listener addresses without recording keys.

## 4. Vultr headless inference

- [ ] Select a model/backend and record image, model digest, context limit,
      timeout, and concurrency limit.
- [ ] Select a Vultr region/plan and record hourly rate, storage, transfer,
      and credit-burn estimate.
- [ ] Review the deployment template with an operator before any create,
      resize, start, stop, or destroy action.
- [ ] Verify `/health` and `/v1/models` from an authorized tailnet peer.
- [ ] Verify one bounded `/v1/chat/completions` request.
- [ ] Verify restart, timeout, unauthorized, over-limit, and backend-failure
      responses.
- [ ] Set a cost alert and define the stop/destroy decision before the pilot.

## 5. Letta opt-in

- [ ] Keep the Letta profile disabled in the default startup.
- [ ] Configure local Postgres/pgvector with a deployment-only password.
- [ ] Point Letta at the private local inference endpoint.
- [ ] Verify Letta is not reachable from the public interface.
- [ ] Verify one bounded local memory read/write using redacted fixture data.
- [ ] Verify stateless Vultr behavior when Letta is stopped.
- [ ] Verify no cloud provider key is required by the Letta profile.

## 6. Phone Basic profile

- [ ] Install only a reviewed health bridge on the target phone.
- [ ] Confirm Android/Termux service binding and Tailscale membership.
- [ ] Run the health smoke test over the tailnet.
- [ ] Confirm the Basic profile has no SMS, camera, contacts, location,
      notifications, flashlight, shell/filesystem, UI automation, arbitrary
      Intent, or model-tool route.
- [ ] Confirm CI uses fixtures and cannot send a phone side effect.
- [ ] Record device ID, runner/model reference, and health evidence without
      copying private phone data.

## 7. Spark escalation

- [ ] Create or select the approved Gemini API project outside the repository.
- [ ] Store the Gemini key in a deployment secret store.
- [ ] Register the approved model and Vesper prompt reference.
- [ ] Enforce the `vesper` / `gmail_algy-alpen` identity mapping.
- [ ] Require an explicit escalation reason and redacted request envelope.
- [ ] Test one disposable approved request.
- [ ] Test rejection for missing approval, prompt reference, model, or
      redaction.
- [ ] Test Gemini outage behavior and confirm it does not route through CMV.
- [ ] Inspect logs for keys, Gmail credentials, raw prompts, and raw outputs.

## 8. Release evidence

- [ ] Attach offline harness results and prohibited-scope scan results.
- [ ] Attach tailnet ACL and public-denial evidence for any disposable pilot.
- [ ] Attach redacted health, model, latency, and failure evidence.
- [ ] Attach cost and shutdown evidence for any Vultr pilot.
- [ ] Record open risks: device SKU/thermal results, backend/model fit,
      Letta retention, and Spark data approval.
- [ ] Update this checklist only through a reviewed spec change when Basic
      capabilities are expanded.

## Definition of done

Basic is complete when:

1. the offline harness passes without external services;
2. the phone contract is health-only;
3. the Vultr interface is tailnet-only and headless;
4. Letta is opt-in and local;
5. Spark is explicit, redacted, and non-CMV;
6. secrets and large artifacts remain outside Git; and
7. all applicable evidence above is attached with no claim that an untested
   deployment is live.

