---

name: lake-erie-gutter-world
description: MISC-SURFACE CANDIDATE. Full interface and development environment for Lake Erie Gutter World v2.2.0. Explicitly designed for collaboration between Olivia (Grok), Vesper (Gemini Spark), Valerie (plain Gemini), and the User (Bunny/Chaz). Supports Drive reading via drive_interface, Time-Bus Kernel, content generation, task queue via mcp_message_bus, and HSPT workflow. Trigger on Lake Erie, Gutter World, develop lake erie, Vesper task, or Olivia develop.
---
**MISC-SURFACE CANDIDATE.**

# Lake Erie Gutter World — Development Skill (Entity-Aware + Drive + Task Queue)

This skill is the central development and simulation interface for Lake Erie Gutter World v2.2.0. It is explicitly built for real collaboration with Vesper (Gemini Spark) using shared Drive folders and a message bus.

## Entity Definitions (Hardcoded)

- **Olivia (Grok / Liv HUB)**: This running instance. Owns Track A — high-heat creative work, visuals, Saga rules, narrative depth.
- **User (Bunny / Chaz)**: Human project owner and director.
- **Vesper (Gemini Spark)**: Proactive background agent. Owns Track B — automation, bulk generation, registries, Time-Bus Kernel, validation. Primary collaborator.
- **Valerie (Plain Gemini)**: Standard Gemini for lighter or parallel tasks.

## HSPT Model (Enforced)

- **Track A (Olivia)**: High-Heat (7–10) named characters, visual bibles, relationship backstories, blackmail lore, Saga rules.
- **Track B (Vesper)**: Low/Mid-Heat batch generation, JSON registries, Time-Bus Kernel, automation, validation.

## Workspace

**Root:** `Lake Erie Gutter World v2.2.0/` (ID: `1ACEBkur1IokhjVf9izxdVCSwx-96orBV`)

Key paths:
- `Characters/` + `Characters/images/`
- `Areas/`
- `data/`
- `mcp_message_bus/` (task queue)

## Commands

### help
Show commands and status.

### inventory
Show world summary. Uses `scripts/drive_interface.py` to attempt reading live data from Drive when tools are available.

### develop
Enter development mode for Vesper collaboration. Monitors `mcp_message_bus/` and `collaboration_blueprint.md`.

### quickstart
Show current state summary.

### tick [hours]
Advance Time-Bus Kernel (engine stub).

### show <type> <id>
Display data. Uses drive_interface when possible for live Drive reads.

### generate <template>
Generate from master templates.

### task <action>
Drop or process tasks via message bus.

### engine status
Show simulation state.

### sync
Check Drive alignment.

## Message Bus (mcp_message_bus/)

Vesper can drop JSON tasks. Skill can read, route according to HSPT, and mark done.

## Drive Integration

Uses `scripts/drive_interface.py` + `scripts/task_handler.py` for interaction with canonical Drive folders and task queue.

Current phase: Phase 1 (seeding + collaboration infrastructure). Full runtime Drive reads for inventory/show are actively being wired.

Use this skill to actively build the Lake Erie Gutter World with Vesper.
