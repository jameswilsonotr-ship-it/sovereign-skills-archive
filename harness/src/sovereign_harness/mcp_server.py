"""Official MCP SDK surface for the offline phone bridge."""

from __future__ import annotations

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:  # MCP SDK v2 renamed FastMCP to MCPServer.
    from mcp.server.mcpserver import MCPServer as FastMCP

from .connectors import PhoneBridgeStub

mcp = FastMCP("sovereign-skills-phone")
_phone = PhoneBridgeStub()


@mcp.tool()
def phone_health() -> dict[str, object]:
    """Return the local phone bridge health fixture."""

    return _phone.health()


@mcp.tool()
def phone_fixture() -> dict[str, object]:
    """Return the offline phone fixture without touching device APIs."""

    return _phone.fixture()


def main() -> None:
    """Run the MCP server over the SDK's default stdio transport."""

    mcp.run()


if __name__ == "__main__":
    main()
