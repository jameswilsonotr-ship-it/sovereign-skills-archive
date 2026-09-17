# Cheapest Vultr Provisioning Runbook: `vc2-1c-2gb`

Status: operator runbook / manual execution only
Scope: one low-cost Vultr Cloud Compute server running the approved
`bridges/vultr` Letta/Ollama Docker Compose stack
Network policy: Tailscale-only for administration and application access
Budget guardrail: **USD $250 hard cap**
Provider/API policy: **This runbook does not authorize live Vultr API, CLI, or
REST calls.** Provision through the Vultr web console unless an owner
explicitly approves another method.

## 0. Read this before touching the provider

This is a procedure, not a permission grant. Reviewing this file, rendering a
Compose configuration, or preparing a local checkout must not create a server,
charge an account, send a credential, or call a provider API.

The local repository currently does not contain `bridges/vultr`. That path is
therefore a required source-of-truth input at execution time, not a claim that
the bridge is present in this checkout. Do not invent a Compose file, service
name, image tag, model name, secret, or port mapping to fill that gap. Obtain
the approved bridge separately and inspect it before deployment.

The `vc2-1c-2gb` plan is a constrained host:

- 1 vCPU and 2 GB RAM leave little room for Docker, a database, Letta, Ollama,
  and a loaded model at the same time.
- A small, quantized model and serialized workloads are assumed.
- The plan is not suitable for large models, concurrent indexing, or
  production availability requirements without an explicit capacity review.
- Vultr prices, regional availability, taxes, bandwidth terms, and plan names
  can change. The amount shown in the web console at order time is the source
  of truth.

**Hard stop conditions**

Stop before creating or modifying infrastructure if any of these is true:

- The checkout or bridge provenance cannot be identified.
- The current quote plus the approved operating window can exceed $250.
- The quote includes backups, snapshots, block storage, managed services, or
  other add-ons that are not in the budget ledger.
- A public application port would be required.
- A Tailscale identity, recovery operator, or out-of-band console path is not
  available.
- The Compose stack has no persistent database/model volume plan.
- The host cannot be reached over Tailscale after bootstrap.
- The intended Ollama model does not fit the remaining memory and disk budget.

## 1. Target architecture

The target is one disposable-but-recoverable VM. It is not a public web
server.

```text
operator workstation
        |
        | SSH / HTTP over Tailscale tailnet only
        v
  Vultr vc2-1c-2gb
  Debian 12 (or the approved bridge OS)
  tailscale0
        |
        +-- Docker Compose network
        |     +-- Letta service
        |     +-- Ollama service
        |     +-- PostgreSQL or other database service required by bridge
        |     +-- volumes defined by the approved bridge
        |
        +-- no public Letta port
        +-- no public Ollama port
        +-- no public database port
```

Preferred access patterns:

1. Use Tailscale SSH for shell access.
2. Use an SSH tunnel over Tailscale for local browser/API access.
3. Use Tailscale Serve only if the operator explicitly needs a tailnet URL
   and has reviewed its access policy.

Do not expose Letta, Ollama, PostgreSQL, Docker, or an admin dashboard on
`0.0.0.0` or the server's public IPv4 address.

## 2. Roles and artifacts

Assign these before provisioning:

| Role | Responsibility |
| --- | --- |
| Request owner | Approves purpose, model, retention, and $250 cap |
| Provisioner | Performs the console and host steps |
| Recovery operator | Holds the Vultr console path and can execute rollback |
| Tailnet admin | Approves the device, ACL/tag, and Tailscale SSH policy |
| Data owner | Approves what enters Letta and what is retained |

Record these in the change ticket or private operations log. Do not put
secrets in this repository.

- Vultr account/project and billing owner
- Region selected and reason
- VM label and immutable deployment identifier
- Tailscale tailnet, device hostname, and ACL/tag
- Approved bridge commit, archive checksum, or release identifier
- Compose images and tags after rendering
- Approved Ollama model and quantization
- Budget window and ledger
- Backup destination and restore owner
- Planned destroy date or renewal decision

## 3. Source and workstation preflight

Perform these checks locally. None of them should contact Vultr. Do not run
the deployment from an uncommitted or unreviewed bridge directory.

### 3.1 Confirm the bridge source

The operator must supply the approved `bridges/vultr` directory, archive, or
repository revision. On a workstation that has it:

```bash
cd /path/to/approved/source
test -d bridges/vultr
find bridges/vultr -maxdepth 2 -type f -print | sort
git -C bridges/vultr status --short 2>/dev/null || true
git -C bridges/vultr rev-parse HEAD 2>/dev/null || true
```

If `bridges/vultr` is not itself a Git checkout, record the archive checksum:

```bash
sha256sum bridges-vultr-approved.tar.gz
```

Review, at minimum:

- `compose.yaml`, `compose.yml`, or `docker-compose.yml`
- `.env.example` or the bridge's documented configuration template
- README and operator notes
- database service and volume declarations
- Letta image/tag and startup command
- Ollama image/tag and model-loading behavior
- health checks and dependency ordering
- published ports
- CPU, memory, and restart settings
- upgrade and backup instructions

### 3.2 Render without starting containers

Run these commands from the approved bridge directory. They validate local
Compose syntax only; they do not provision a server.

```bash
cd bridges/vultr
cp .env.example /tmp/vultr-stack.env.review  # if the bridge provides one
# Fill review-only placeholders in a disposable copy; never use production secrets.
docker compose --env-file /tmp/vultr-stack.env.review config --quiet
docker compose --env-file /tmp/vultr-stack.env.review config --services
docker compose --env-file /tmp/vultr-stack.env.review config --images
docker compose --env-file /tmp/vultr-stack.env.review config > /tmp/vultr-stack.rendered.yml
```

If the bridge has no `.env.example`, do not guess its variables. Ask the
bridge owner for a non-secret template, then repeat the render.

Inspect the rendered output privately. It may contain interpolated secrets:

```bash
less /tmp/vultr-stack.rendered.yml
```

Before proceeding, answer all of these from the actual rendered file:

- What are the exact Letta, Ollama, and database service names?
- Which service stores Letta state?
- Which service stores Ollama models?
- Are volumes named and persistent?
- What health checks exist?
- What ports are published?
- Do any ports bind to all interfaces?
- Does Letta reach Ollama by Compose service name or host address?
- Does the bridge require a separate migration/init command?
- What is the documented supported model?

### 3.3 Validate the low-memory plan

Use the bridge's actual images and model requirements. Do not assume a model
fits because its download is small: runtime memory is often larger than the
file size.

Create a small capacity note with:

```text
host RAM                       2 GB
- OS and tailscaled reserve    [measured/estimated]
- Docker and database reserve  [measured/estimated]
- Letta reserve                [measured/estimated]
- Ollama server reserve        [measured/estimated]
- model runtime reserve        [vendor/test measurement]
= remaining safety margin      [must be positive]
```

The first boot should load no model larger than the approved capacity note.
Do not run an import, embedding job, model pull, and database migration at the
same time on this plan.

## 4. Budget gate: $250, no exceptions

The $250 limit is the total approved spend for the chosen operating window,
not merely the advertised compute line item.

### 4.1 Build the ledger before ordering

Copy this table into the change record and fill it from the Vultr web-console
quote and the approved service terms. Do not use an API response as a
substitute for the displayed checkout total.

| Cost item | Rate | Quantity/window | Expected total | Confirmed? |
| --- | ---: | ---: | ---: | --- |
| `vc2-1c-2gb` compute | `$____ / month` | `____ months` | `$____` | [ ] |
| IPv4, if separately charged | `$____` | `____` | `$____` | [ ] |
| Backups | `$____ / month` | `0 unless approved` | `$____` | [ ] |
| Snapshots | `$____` | `0 unless approved` | `$____` | [ ] |
| Block storage | `$____ / month` | `0 unless approved` | `$____` | [ ] |
| Bandwidth overage | `$____` | `0 unless approved` | `$____` | [ ] |
| Taxes/fees | `$____` | `as quoted` | `$____` | [ ] |
| Domain or other services | `$____` | `0 unless approved` | `$____` | [ ] |
| Contingency | `$____` | required | `$____` | [ ] |
| **Landed total** |  |  | **$____** | [ ] |

Use this conservative formula:

```text
landed_total =
  (compute_rate × months)
  + (approved_add_on_rates × months)
  + one_time_fees
  + expected_tax
  + bandwidth_overage_reserve
  + contingency
```

Proceed only when:

```text
landed_total <= 250.00
```

Use a non-zero contingency. If a quote only fits by assuming zero taxes,
zero overage, or a promotional rate that is not documented, it does not pass
the gate.

An illustrative calculation is not a current price assertion:

```text
illustration only:
  $10/month × 12 months = $120
  $10/month × 24 months = $240
  remaining headroom must still cover tax, fees, and contingency
```

### 4.2 Budget checklist

- [ ] Compute plan is exactly `vc2-1c-2gb`, not a larger default.
- [ ] Region availability and current rate were checked in the web console.
- [ ] Billing period is recorded.
- [ ] No automatic backups were selected unless budgeted.
- [ ] No snapshot was created during testing unless budgeted.
- [ ] No block storage or managed database was attached.
- [ ] No extra IPv4, floating IP, load balancer, DNS, or domain was added.
- [ ] Bandwidth assumptions are documented.
- [ ] Tax and fees are included or conservatively reserved.
- [ ] Tailscale cost is recorded according to the applicable tailnet plan.
- [ ] At least 10% or another owner-approved contingency remains.
- [ ] The destroy date is on the calendar.
- [ ] A second person approved the landed total.
- [ ] A screenshot or invoice reference is stored privately, not in Git.

**Stop if the web-console checkout total is unclear.** Do not create the
server and “check the bill later.”

## 5. Provision through the Vultr web console

These are manual UI actions. They are intentionally not translated into
Vultr API, CLI, Terraform, or raw HTTP calls.

1. Open the correct Vultr account and project in the web console.
2. Confirm the project and billing owner match the change record.
3. Choose Cloud Compute.
4. Choose the region approved in the budget/capacity note.
5. Choose the exact `vc2-1c-2gb` plan.
6. Choose the approved Debian release or the operating system required by the
   bridge. Record the image version.
7. Add the provisioner's SSH public key. Never paste a private key.
8. Disable password authentication if the console offers that option.
9. Set a unique, non-sensitive hostname/label. Do not put tokens or customer
   data in the label.
10. Do not select backups, snapshots, block storage, a load balancer, or
    unrelated marketplace software.
11. Review the final quote against the signed-off ledger.
12. Take a private screenshot or record the invoice/reference number.
13. Create the single server only after the budget gate is checked.
14. Do not begin application setup from the public IP. Use it only for the
    temporary bootstrap connection described below.

Keep the Vultr browser tab and console access available for rollback. Do not
close the recovery path after Tailscale appears healthy.

## 6. Bootstrap the host with a narrow temporary perimeter

The bootstrap perimeter exists only long enough to install and validate
Tailscale. It is not the final security posture.

### 6.1 Vultr firewall during bootstrap

In the web console, attach or create a firewall group with the smallest
possible rules:

- TCP 22 from the provisioner's current public IP as `/32` only.
- Established/related return traffic, if the console models it separately.
- No TCP 80, 443, 8283, 11434, 5432, or other application/database ports.
- No UDP application ports.
- Outbound access only as required for package installation and Tailscale.

If the provisioner's public IP changes, use the Vultr console rather than
opening SSH to the world. Remove the temporary rule after Tailscale works.

### 6.2 First login and baseline capture

Use the provider-generated public address only for this bootstrap session:

```bash
ssh -o IdentitiesOnly=yes root@<temporary-public-ip>
```

Immediately capture a baseline without putting secrets in the log:

```bash
hostnamectl
cat /etc/os-release
uname -a
free -h
df -h
ip -brief address
ss -lntup
```

Create a non-root operator account, install the approved SSH key, and verify
that the account works before disabling root/password access:

```bash
adduser --disabled-password --gecos "" <operator-user>
usermod -aG sudo <operator-user>
install -d -m 700 -o <operator-user> -g <operator-user> /home/<operator-user>/.ssh
install -m 600 -o <operator-user> -g <operator-user> /path/to/approved_authorized_keys \
  /home/<operator-user>/.ssh/authorized_keys
```

The path to `authorized_keys` above is illustrative. Transfer the public key
through the approved bootstrap method; never put a private key on the host.

From a second workstation shell, verify:

```bash
ssh -o IdentitiesOnly=yes <operator-user>@<temporary-public-ip> true
```

Only after that succeeds, apply the SSH policy required by the OS baseline:

```text
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
```

Validate the SSH configuration before restarting it:

```bash
sshd -t
systemctl reload ssh
```

Keep the existing session open until the new session is confirmed.

## 7. Install Docker Compose and host prerequisites

Use the Docker installation method approved by the bridge or organization.
Pin versions where the bridge supplies pins. The commands below are a
procedure outline; review package origins and versions before execution.

Install basic host packages:

```bash
apt-get update
apt-get install -y ca-certificates curl git jq rsync ufw unattended-upgrades
```

Install Docker Engine and the Compose plugin from the approved repository,
then verify without starting the application:

```bash
docker version
docker compose version
systemctl is-enabled docker
systemctl is-active docker
```

Do not add the operator to the `docker` group without accepting that membership
is effectively root-equivalent. Prefer `sudo docker ...` for a small
single-operator host.

### 7.1 Optional swap, with an explicit trade-off

On a 2 GB host, a small swap file can reduce abrupt OOM kills but will make
model inference and migrations slower. It does not make an oversized model
fit safely.

If the owner approves swap:

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
printf '/swapfile none swap sw 0 0\n' >> /etc/fstab
sysctl vm.swappiness=10
```

Record the choice. Do not silently add swap to hide a failed capacity plan.

## 8. Make Tailscale the only access path

### 8.1 Install Tailscale from an approved package source

Use the organization's package provenance policy. If the documented install
method downloads a script, download it, inspect it, and then run the inspected
file; do not blindly pipe an unreviewed script to a shell.

After installation:

```bash
systemctl enable --now tailscaled
tailscale version
```

### 8.2 Enroll without exposing the auth key

Use a short-lived, tagged, least-privilege auth key supplied through the
approved secret channel. Do not commit it, paste it into chat, put it in
`.env`, or leave it in shell history.

One safe shell pattern is:

```bash
read -r -s TS_AUTH_KEY
printf '\n'
sudo tailscale up \
  --auth-key="$TS_AUTH_KEY" \
  --hostname=<tailnet-hostname> \
  --ssh
unset TS_AUTH_KEY
```

Use the exact ACL/tag policy approved by the tailnet administrator. If the
tailnet does not permit Tailscale SSH, omit `--ssh` and use ordinary SSH over
the Tailscale address with the host firewall restricted to `tailscale0`.

Verify:

```bash
tailscale status
tailscale ip -4
tailscale netcheck
```

From the operator workstation, connect by the tailnet DNS name or Tailscale
IP, not the public address:

```bash
ssh <operator-user>@<tailnet-hostname>
```

Do not continue until the Tailscale connection works from the intended
operator device.

### 8.3 Close the bootstrap perimeter

In the Vultr web console:

1. Replace the temporary public-IP `/32` SSH rule with no public SSH rule.
2. Keep no application or database ingress rules.
3. Leave only the outbound policy required by the host and Tailscale.
4. If direct Tailscale peer connections are desired, allow UDP 41641 only
   when the tailnet policy and owner approve it. It is not an application
   port and is not required for all connections.
5. Apply the firewall change and verify the existing Tailscale session.

On the host, set a default-deny inbound policy and allow only the Tailscale
interface for administration:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow in on tailscale0 to any port 22 proto tcp
ufw --force enable
ufw status verbose
```

If Tailscale SSH is enabled and the bridge requires no host SSH, the port 22
rule can be omitted after testing the approved Tailscale SSH policy. Never
enable UFW until a known-good Tailscale recovery session exists.

Confirm the public interface has no application listeners:

```bash
ss -lntup
```

A listener on `0.0.0.0:8283`, `0.0.0.0:11434`, `0.0.0.0:5432`, or an
equivalent stack port is a failure. Stop and correct it before starting the
stack.

## 9. Transfer and install `bridges/vultr`

Transfer only the approved, reviewed bridge revision. Do not clone arbitrary
branches directly onto the server.

Example using the already-established Tailscale path:

```bash
sudo install -d -m 0750 -o root -g root /opt/bridges
rsync -a --delete \
  --exclude '.env' \
  --exclude '*.key' \
  --exclude '*.pem' \
  bridges/vultr/ \
  <operator-user>@<tailnet-hostname>:/tmp/bridges-vultr/
```

On the server:

```bash
sudo install -d -m 0750 /opt/bridges/vultr
sudo rsync -a --delete /tmp/bridges-vultr/ /opt/bridges/vultr/
sudo rm -rf /tmp/bridges-vultr
cd /opt/bridges/vultr
```

Record the bridge revision/checksum on the server:

```bash
git rev-parse HEAD 2>/dev/null || sha256sum compose.y*ml docker-compose.y*ml
```

If the bridge includes a deployment-specific `.env.example`, make a root-only
runtime copy and populate it through the approved secret manager:

```bash
sudo install -m 600 /dev/null /opt/bridges/vultr/.env
sudo chown root:root /opt/bridges/vultr/.env
```

Required values must come from the bridge documentation. Typical categories
include database credentials, Letta authentication, an internal Ollama URL,
and a model identifier. The categories are not permission to invent variable
names or defaults.

Check permissions:

```bash
stat -c '%a %U:%G %n' /opt/bridges/vultr /opt/bridges/vultr/.env
```

## 10. Compose preflight on the server

Run from `/opt/bridges/vultr` with the real runtime environment loaded. These
steps render and inspect; they should not start containers.

```bash
cd /opt/bridges/vultr
sudo docker compose config --quiet
sudo docker compose config --services
sudo docker compose config --images
sudo docker compose config > /tmp/vultr-stack.rendered.yml
```

Review the rendered configuration privately. Then check the following:

- Images use approved tags or immutable digests.
- No image is unexpectedly `latest`.
- Database and model volumes are persistent.
- Restart policy will not create an uncontrolled crash loop.
- Health checks do not claim readiness before the service is usable.
- Required secrets are present without being printed into an operations log.
- Published ports are either absent or bound to `127.0.0.1`.
- No Compose `network_mode: host` is present unless separately reviewed.
- No container mounts the Docker socket unless separately approved.
- No container runs privileged without a written exception.

If the source bridge publishes ports on all interfaces, fix the bridge
configuration through its normal review process or use a reviewed deployment
override. Do not improvise a one-off production file that cannot be reproduced.

For a local-only service, the rendered mapping should resemble:

```yaml
ports:
  - "127.0.0.1:<host-port>:<container-port>"
```

The exact service and port names must come from the approved bridge. This
snippet is a policy example, not a replacement for the bridge file.

## 11. Start the stack in dependency order

The exact service names are bridge-owned. Discover them first:

```bash
sudo docker compose config --services
```

Start only the database or dependency service(s) documented by the bridge:

```bash
sudo docker compose up -d <database-service>
sudo docker compose ps
```

Wait for its health check and perform the bridge's documented initialization
or migration step. Do not run a destructive database reset. If no health
check exists, use the bridge's documented readiness command and record the
result.

Start Ollama next:

```bash
sudo docker compose up -d <ollama-service>
sudo docker compose ps
sudo docker compose logs --since=5m <ollama-service>
```

Pull only the owner-approved small model, using the exact service and model
from the bridge instructions:

```bash
sudo docker compose exec <ollama-service> ollama pull <approved-model>
```

Do not pull multiple models “for testing” on this disk and memory budget.
Confirm the model is present:

```bash
sudo docker compose exec <ollama-service> ollama list
```

Start Letta last:

```bash
sudo docker compose up -d <letta-service>
sudo docker compose ps
sudo docker compose logs --since=5m <letta-service>
```

Use the bridge's documented health endpoint or readiness command from the
host-local path. Example shape only:

```bash
curl --fail --silent --show-error http://127.0.0.1:<letta-port>/health
```

If the bridge does not document a health endpoint, inspect container health
and logs instead. Do not publish a port merely to make health checking easy.

### 11.1 Memory and disk checks

Run checks while the stack is idle and during one controlled inference:

```bash
free -h
df -h
sudo docker stats --no-stream
sudo docker compose ps
```

Stop the rollout if the host swaps continuously, the kernel reports OOM
kills, the database is unhealthy, or free disk falls below the owner-approved
reserve. A green `docker compose ps` alone is not a capacity sign-off.

## 12. Access the services without public ports

### 12.1 SSH tunnels over Tailscale

Keep application ports bound to loopback on the VM. From the operator
workstation, open a tunnel through the Tailscale hostname:

```bash
ssh -N \
  -L <local-letta-port>:127.0.0.1:<remote-letta-port> \
  -L <local-ollama-port>:127.0.0.1:<remote-ollama-port> \
  <operator-user>@<tailnet-hostname>
```

Use the local forwarded ports in the browser or client. Do not change the
Compose binding to the public IP to avoid using a tunnel.

### 12.2 Optional Tailscale Serve

Tailscale Serve can publish a local service to the tailnet, but it changes the
access surface and may interact with tailnet ACLs. Use it only if the owner
approves it and the exact command/policy is recorded. Never use Funnel or
another public relay for this stack.

## 13. Verification checklist

Complete the checklist in order and attach results to the private change
record. Redact secrets, tokens, full environment files, and customer data.

### Network and access

- [ ] Tailscale device appears in the correct tailnet.
- [ ] Tailscale ACL/tag is correct.
- [ ] Tailscale SSH or SSH over `tailscale0` works for the operator.
- [ ] Public SSH bootstrap rule was removed.
- [ ] No public Letta port is reachable.
- [ ] No public Ollama port is reachable.
- [ ] No public database port is reachable.
- [ ] `ss -lntup` shows only loopback or Tailscale-approved listeners.
- [ ] The operator can access the services through the approved tunnel/path.

### Compose and data

- [ ] `docker compose config --quiet` passes.
- [ ] Rendered images and tags were reviewed.
- [ ] Database volume exists and is not an anonymous throwaway volume.
- [ ] Ollama model volume exists and has enough free space.
- [ ] Letta starts after its dependencies.
- [ ] Letta can reach Ollama using the internal Compose address.
- [ ] A single small inference succeeds.
- [ ] No OOM or restart loop occurred.
- [ ] Logs contain no unexpected secret disclosure.

### Operations

- [ ] Health/readiness evidence is recorded.
- [ ] A non-destructive database backup was created and verified.
- [ ] Restore procedure identifies the exact service/volume names.
- [ ] Owner-approved destroy date is recorded.
- [ ] Current landed budget is below $250 with contingency.
- [ ] Recovery operator can reach the Vultr web console.
- [ ] The approved bridge revision is recorded.

## 14. Backup and restore rehearsal

Do not call a volume “backed up” because it exists. Backups must be readable
outside the VM and restorable without destroying the source.

Use the bridge's documented database service and credentials. The following is
an example shape for PostgreSQL; substitute the actual service and database
names after review:

```bash
mkdir -p /var/backups/vultr-stack
chmod 700 /var/backups/vultr-stack
sudo docker compose exec -T <database-service> \
  pg_dump -U <database-user> -d <database-name> --format=custom \
  > /var/backups/vultr-stack/letta-$(date -u +%Y%m%dT%H%M%SZ).dump
sha256sum /var/backups/vultr-stack/*.dump
```

Copy the encrypted backup to the approved external destination over the
approved Tailscale path or storage mechanism. Do not store the only copy on
the VM. Verify:

- the backup file can be downloaded;
- the checksum matches;
- the restore owner knows the database version and commands;
- the restore has been rehearsed in an isolated disposable directory or host.

Never remove Compose volumes during a first rollback attempt. `down -v` is a
destructive command and is prohibited in this runbook unless the data owner
has explicitly approved data deletion.

## 15. Upgrade procedure

Treat image changes, model changes, and bridge changes as separate changes.

1. Confirm the new bridge revision and image digests.
2. Re-render the Compose file locally and on the host.
3. Re-run the $250 forecast if the change adds storage, runtime, or services.
4. Capture a database backup and current `docker compose ps`.
5. Record the current image IDs and volume names.
6. Stop new ingestion and wait for active work to finish.
7. Upgrade one dependency at a time.
8. Verify database health.
9. Verify Ollama and the approved model.
10. Verify Letta readiness and one controlled inference.
11. Watch memory, disk, and logs.
12. Keep the previous image/bridge revision available until sign-off.

Do not use `docker compose pull` or an unpinned `latest` tag as an upgrade
policy. The exact image change must be reviewable and reproducible.

## 16. Rollback runbook

Rollback is chosen by failure class. Preserve evidence before deleting
anything.

### 16.1 Application or image regression

1. Announce the rollback and stop new client traffic through the tunnel.
2. Capture:

   ```bash
   sudo docker compose ps
   sudo docker compose logs --since=30m > /tmp/vultr-stack-failure.log
   free -h
   df -h
   sudo docker stats --no-stream
   ```

3. Stop only the affected service if dependencies can remain healthy:

   ```bash
   sudo docker compose stop <affected-service>
   ```

4. Restore the previously approved bridge revision or image digest.
5. Re-render with `docker compose config --quiet`.
6. Start dependencies first, then Ollama, then Letta.
7. Verify health, one controlled inference, memory, and logs.
8. Keep existing volumes. Do **not** run `docker compose down -v`.
9. Record the failure and leave the bad revision disabled.

### 16.2 Database migration failure

1. Stop Letta and any writer service.
2. Do not delete or recreate the database volume.
3. Capture database logs and migration output.
4. Restore the prior bridge revision if it is compatible.
5. If data is damaged, restore the verified backup into an isolated database
   first, then obtain data-owner approval before replacing anything.
6. Re-run the documented migration only after the rollback path is tested.

The database service name and volume name must come from the actual bridge.
Never use a guessed volume name in a destructive command.

### 16.3 OOM, disk pressure, or runaway model

1. Stop the model pull or inference.
2. Stop Letta before the database if memory must be reclaimed.
3. Preserve logs and `docker inspect` output.
4. Do not delete the model or database volume until the owner chooses what
   data may be removed.
5. Remove only the unneeded, approved model using the bridge's documented
   method.
6. If the approved model cannot run within 2 GB, stop the rollout. Do not
   “solve” it by removing safeguards or enabling public access.

### 16.4 Tailscale or firewall lockout

Use the Vultr web console, not a public firewall broadening, as the recovery
path.

1. Open the provider console.
2. Inspect `tailscaled`, `ufw`, routes, and recent changes.
3. Restore the last known-good Tailscale/host firewall policy.
4. Keep application ports closed while access is repaired.
5. Verify a new Tailscale session from the operator workstation.
6. Remove any temporary public SSH exception as soon as the session works.

Do not run `tailscale down` over your only remote session unless the provider
console is open and the recovery operator is present.

### 16.5 Full infrastructure rollback

Use this when the host is unrecoverable, the budget is threatened, or the
owner cancels the deployment.

1. Stop the Compose stack without removing volumes:

   ```bash
   sudo docker compose stop
   ```

2. Create and verify the final approved backup if data retention requires it.
3. Record the server ID, invoice, bridge revision, and final evidence.
4. In the Vultr web console, destroy the server.
5. Separately remove snapshots, block storage, floating IPs, or other
   billable resources if any were accidentally created.
6. Remove the device from the tailnet and revoke the enrollment key.
7. Confirm the Vultr project has no remaining billable resources.
8. Confirm the next invoice/usage view reflects the expected result.
9. Mark the change rolled back and retain the evidence privately.

If the server is destroyed before the backup is verified, data recovery is not
assumed. That is why the backup and destroy steps are separate gates.

## 17. Final handoff

The run is complete only when all of the following are true:

- [ ] The exact plan and region are recorded.
- [ ] The current landed budget and cap check are recorded.
- [ ] The bridge revision/checksum is recorded.
- [ ] Tailscale-only access is demonstrated.
- [ ] Public app/database access is tested and absent.
- [ ] Compose configuration is rendered and reviewed.
- [ ] Letta, Ollama, and the bridge database are healthy.
- [ ] The approved model runs one controlled request.
- [ ] Resource headroom is documented.
- [ ] Backup and restore ownership are assigned.
- [ ] Rollback evidence and provider console access are confirmed.
- [ ] Destroy/renewal date is recorded.

The handoff must not include private keys, Tailscale auth keys, database
passwords, Letta tokens, full `.env` files, or unredacted customer data.

## Appendix A: operator command checklist

This compact list is for an already-approved execution. It is not a
substitute for the gates above.

```text
[ ] Confirm bridge source and revision
[ ] Render Compose locally; inspect service names, images, ports, volumes
[ ] Complete $250 landed-cost ledger with contingency
[ ] Provision exact vc2-1c-2gb in the web console
[ ] Add SSH key; use temporary /32 bootstrap SSH rule
[ ] Create non-root operator; disable root/password login
[ ] Install Docker Compose and approved host packages
[ ] Install/enroll Tailscale with least-privilege key
[ ] Verify Tailscale access from operator workstation
[ ] Remove public bootstrap SSH rule
[ ] Enable host firewall; allow only approved Tailscale administration
[ ] Transfer approved bridges/vultr revision
[ ] Create root-only runtime .env from the bridge template
[ ] Render Compose on host; reject public ports and unsafe privileges
[ ] Start database and complete documented init/migration
[ ] Start Ollama; pull only the approved small model
[ ] Start Letta; verify internal Ollama connectivity
[ ] Test through an SSH tunnel over Tailscale
[ ] Capture health, memory, disk, and logs
[ ] Create and verify a non-destructive backup
[ ] Record handoff, rollback, and destroy date
```

## Appendix B: explicit prohibitions

- No Vultr API, CLI, Terraform, or raw HTTP provisioning from this runbook.
- No server creation before the $250 ledger is approved.
- No public Letta, Ollama, database, Docker, or admin ports.
- No secrets in Git, chat, shell history, or pasted logs.
- No guessed service names, environment variables, ports, model names, or
  volume names.
- No `docker compose down -v` during ordinary rollback.
- No unreviewed `latest` image or model tag.
- No destructive restore or volume replacement without data-owner approval.
- No public Funnel/relay path for the stack.
- No treating a green container status as proof of capacity or backup health.
