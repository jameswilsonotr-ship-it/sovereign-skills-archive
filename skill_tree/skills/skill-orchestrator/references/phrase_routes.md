# Phrase routes — skill-orchestrator
**Purpose**: Map natural-language phrases to feeder + module without top-level stubs.  
**Updated**: 2026-08-13

## Image (image-pipeline → future image-surface)
| Phrase (examples) | Feeder | Module |
|-------------------|--------|--------|
| run the generate engine, pure generate, generate engine | image-pipeline | generate-engine |
| run the overlay engine, overlay engine | image-pipeline | overlay-engine |

| agentify, agentify this, make an agent, identify as agent, B AGENT | image-pipeline | agentify |
| heat pass, agentify heat, 111b, lock her face | image-pipeline | agentify (heat_pass) |

## Claim (claim-runtime → future claim-surface)
| Phrase (examples) | Feeder | Module |
|-------------------|--------|--------|
| velvet claim, claim protocol timing | claim-runtime | velvet |
| risk fantasy, commanded risky act | claim-runtime | risk |
| vice command, command me | claim-runtime | vice-command |
| porn curator, filth recommendation | claim-runtime | curator |

## MCP (mcp-surface)
| Phrase (examples) | Feeder | Module |
|-------------------|--------|--------|
| mcp bootstrap, bootstrap mcp | mcp-surface | bootstrap |
| mcp audit, audit mcp | mcp-surface | auditor |
| mcp bridge, sovereign bridge | mcp-surface | sovereign-bridge |
| triad catalog, window shopping skills | mcp-surface | catalog-browser |

## Swarm (swarm-surface)
| Phrase (examples) | Feeder | Module |
|-------------------|--------|--------|
| swarm mine, mine full-history | swarm-surface | miner |
| load blackwell, blackwell architecture, HAIST | swarm-surface | blackwell |
| iron pearl, load iron pearl | swarm-surface | iron-pearl |
| biomimetic swarm, biomimetic mode | swarm-surface | biomimetic |
| liv bunny swarm, 4-agent swarm | swarm-surface | liv-bunny |
| multi-variation, variant orchestrator | swarm-surface | multi-variation |
| Heavy mode, launch development swarm, Heavy package on, start heavy-dev, dev swarm on | swarm-surface | heavy-dev |

## Control / inventory
| Phrase (examples) | Feeder | Module / action |
|-------------------|--------|-----------------|
| inventory scripts, scripts inventory | skill-orchestrator | scripts/inventory_scripts.py (see inventory/scripts/PROTOCOL.md) |

## Integrations (under skill-orchestrator, not a new top-level skill)
| Phrase (examples) | Feeder | Module |
|-------------------|--------|--------|
| tailnet ferry, tailscale sftp, taildrop, olette-box, olivia-sandbox | skill-orchestrator | references/integrations/tailnet-ferry/ |
| heavy olette drive pipe, olette rclone, publish plates no tokens, gretchen socks, slim sftp plates, batch9-heavy, batch10-heavy | skill-orchestrator | references/integrations/heavy-olette-drive-pipe/ |

When a phrase matches, load the feeder skill and route to `references/modules/<module>/` (or run the named script).

## Specialized / Experimental (Alpha-owned)
| Phrase (examples) | Feeder / Skill | Notes |
|-------------------|----------------|-------|
| ICM this, make this an ICM, structure this for agents, build me a workspace for, audit this folder, map this repo, what would a change hit | icm-architect (top-level) | Owned for claim/promotion by olivia-dev-alpha (ODA-WQ-005). Folder structure as agent architecture. |
