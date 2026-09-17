# Vultr tailnet-only MCP host

[`cloud-init.mcp-host.example.yaml`](cloud-init.mcp-host.example.yaml) is a
bootstrap sketch for a fresh Vultr Linux instance. It:

1. installs and starts Tailscale;
2. joins the tailnet using an injected deployment secret;
3. enables a placeholder MCP service; and
4. binds the service to the VPS `100.x` Tailscale address while restricting
   the MCP port to the Tailscale CGNAT range.

[`mcp-host.config.example.json`](mcp-host.config.example.json) is the
Pydantic-validated, network-free contract behind the sketch.

Before use, replace all angle-bracket values through the deployment system,
install the actual MCP host at `/opt/mcp-host`, and review the host firewall
and Tailscale ACL policy. The auth secret must be injected at deploy time and
must not be committed here.

The sketch deliberately does not claim that the MCP application is installed.
The final service must preserve the same bind address and tailnet-only
firewall rule.
