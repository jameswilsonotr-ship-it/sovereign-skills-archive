# Offline bridge deployment stubs

These files describe the smallest safe network surfaces for the phone and VPS
bridges. They are templates, not live credentials or a live MCP deployment.
The test suite validates the JSON templates without opening a network
connection.

## Surfaces

- [Termux phone health bridge](termux-phone-mcp/README.md): a deployable
  `termux-services` run script for `GET /health` on the phone's Tailscale
  address and port `8081`.
- [olette-box SFTP template](sftp/README.md): OpenSSH aliases and a typed sync
  manifest for `100.115.0.111:22`, with key paths only for `bunny` and
  `olivia`.
- [Vultr MCP host sketch](vultr/README.md): cloud-init and service templates
  that bind the MCP listener to the VPS Tailscale address only.

The phone module itself lives in
[`harness/src/sovereign_harness/phone_mcp.py`](../harness/src/sovereign_harness/phone_mcp.py).
Run the offline checks from `harness/` with `pytest`.

## Safety boundaries

- Replace angle-bracket values during deployment; do not commit credentials,
  private key bytes, or Tailscale authentication material.
- Keep the phone and VPS listeners bound to a `100.x` Tailscale address.
- The bridge stubs expose health/configuration surfaces only. They do not send
  SMS, access cameras, or perform live network checks in CI.
