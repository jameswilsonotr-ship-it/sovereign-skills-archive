# Termux phone health bridge

The existing Python module provides the offline-safe endpoint:

```text
GET http://<TAILSCALE_PHONE_IP>:8081/health
```

It returns the `phone-bridge` readiness payload and intentionally has no SMS
or camera capability. `phone-bridge.config.example.json` records the contract
validated by the harness.

## Install on Termux

1. Install Termux, Tailscale, Python, and `termux-services`.
2. Clone this repository on the phone, create `harness/.venv`, and install the
   harness package with its runtime dependencies.
3. Copy [`run.sh`](run.sh) to
   `$PREFIX/var/service/phone-mcp/run`, then make it executable:

   ```sh
   mkdir -p "$PREFIX/var/service/phone-mcp"
   cp bridges/termux-phone-mcp/run.sh "$PREFIX/var/service/phone-mcp/run"
   chmod 700 "$PREFIX/var/service/phone-mcp/run"
   ```

4. Enable the service from a Termux shell:

   ```sh
   sv-enable phone-mcp
   sv status phone-mcp
   ```

The script resolves the phone's IPv4 Tailscale address with `tailscale ip -4`
and refuses to start when it cannot obtain a `100.x` address. Set
`PHONE_MCP_ROOT` if the checkout is not at
`$HOME/sovereign-skills-archive`, or set `PHONE_MCP_PYTHON` to the Python
interpreter in the prepared virtual environment.

This is a tailnet-bound listener, not an internet-facing service. Confirm
Tailscale ACLs before allowing a client to call `/health`.
