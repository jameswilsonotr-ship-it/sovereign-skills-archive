# MCP sidecar connections

The inference container is not the MCP sidecar. Keep those responsibilities
separate:

```text
phone MCP :8081  <-- encrypted Tailscale path -->  VPS MCP sidecar
                                                   |
                                                   +-- SSH/SFTP --> olette-box
```

The sidecar makes outbound connections only. It does not publish a second
public listener, and it should not expose the phone or Olette-box through
the OpenAI-compatible inference port.

## Phone MCP on `:8081`

Install the actual MCP client/sidecar separately, then configure its phone
upstream with deployment-only values similar to:

```dotenv
PHONE_MCP_URL=http://__PHONE_TAILNET_IP__:8081
PHONE_MCP_HEALTH_URL=http://__PHONE_TAILNET_IP__:8081/health
PHONE_MCP_ENDPOINT=http://__PHONE_TAILNET_IP__:8081/mcp
```

The exact MCP path and transport must match the phone service. The existing
phone bridge template documents the health surface; a successful health
response does not by itself prove that an MCP session endpoint is enabled.
From the VPS, validate reachability without sending a tool call:

```sh
curl --fail --silent --show-error \
  "http://__PHONE_TAILNET_IP__:8081/health"
```

Use a Tailscale ACL to allow the VPS identity to reach only the phone's MCP
port. Keep the phone service bound to its `100.x` address, and require
application authentication if the MCP implementation supports it. Do not
use `0.0.0.0:8081` as a shortcut.

## Olette-box over SFTP

Use SSH/SFTP from the sidecar to Olette-box on the tailnet. The repository
already provides the client-side starting points in
[`../sftp/README.md`](../sftp/README.md),
[`../sftp/olette-box.ssh-config.example`](../sftp/olette-box.ssh-config.example),
and the typed sync manifest. Copy those templates to a deployment-only
location, install the private key out of band with mode `0600`, and add the
trusted host fingerprint to `known_hosts`.

Example deployment-only environment:

```dotenv
OLETTE_BOX_SFTP_ALIAS=olette-box-bunny
OLETTE_BOX_SFTP_REMOTE_DIR=__REMOTE_DIRECTORY__
OLETTE_BOX_SFTP_CONFIG=/etc/mcp-sidecar/olette-box.ssh-config
OLETTE_BOX_SFTP_KNOWN_HOSTS=/etc/mcp-sidecar/known_hosts
```

The example aliases intentionally use key-path placeholders. The sidecar
should use a dedicated account, a least-privilege key, strict host-key
checking, and an explicit remote directory:

```sh
sftp -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=/etc/mcp-sidecar/known_hosts \
  -F /etc/mcp-sidecar/olette-box.ssh-config \
  olette-box-bunny
```

If the sidecar needs a non-interactive transfer, use a narrowly scoped
manifest and an SFTP batch file. Do not put key bytes, passwords, or file
contents in this repository or in inference prompts. Prefer read-only
credentials until a write operation has been explicitly reviewed.

## Network and secret boundaries

- Run the sidecar with access to the host's Tailscale route; host networking
  is the simplest option when the sidecar is containerized.
- Permit only VPS-to-phone `8081` and VPS-to-Olette-box SSH/SFTP in the
  Tailscale ACL and host firewall.
- Keep `TS_AUTHKEY`, Vultr tokens, MCP credentials, SSH private keys, and
  `known_hosts` out of `docker-compose.yml` and Git.
- Test the two paths independently before enabling an MCP tool that can
  write files or invoke phone actions.
- This document does not provision Vultr, call an MCP tool, sync SFTP, or
  read a live `SKILL.md`.
