# CHEW ROSTER

Atomic included-burn routing for Hi Cursor agents. Each agent owns exactly one
OpenSpec change-id.

| Hi Cursor agent | OpenSpec change-id |
| --- | --- |
| Meter Watch | `meter-watch` |
| Burn Chew Lanes | `burn-chew-lanes` |
| Vultr Gateway Docs | `vultr-gateway-docs` |
| Iron Pearl SSOT | `iron-pearl-ssot` |
| Phone MCP HUD | `phone-mcp-hud` |
| Burn Flip Cutover | `burn-flip-cutover` |

## Apply rule

Run `/openspec-apply` with one change-id only. A Hi Cursor agent must apply
only its assigned change-id from the roster; do not combine multiple
change-ids in one `/openspec-apply` invocation.
