---
name: mcp-bootstrap-test-suite
version: 0.1.0
description: Test suite for validating MCP Bootstrap, Auditor, and Repo-Sniffer behavior across fresh conversations. Designed to be run manually at the start of new chats to confirm the sovereign stack is loading correctly.
tags: [mcp, bootstrap, test, audit, sovereign]
---

# MCP Bootstrap + Auditor Test Suite

## Purpose
This document defines a repeatable set of tests to verify that the foundational MCP skills (`mcp-bootstrap`, `mcp-auditor`, `repo-sniffer`, `mcp-sovereign-bridge`) are correctly loaded and behaving as expected at the start of new conversations.

## Test Environment
- Fresh Grok conversation (new thread recommended)
- User has the persistent skills installed in `~/.grok/skills/`
- Optional: Repo-Sniffer MCP server running locally and connected via Custom connector

## Test 1: Bootstrap Skill Visibility (Critical)
**Goal**: Confirm `mcp-bootstrap` is loaded and active at conversation start.

**Steps**:
1. Start a brand new conversation.
2. Immediately say: "Confirm MCP Bootstrap is loaded."
3. Expected behavior:
   - Grok acknowledges the skill.
   - Offers to help spin up a fresh MCP server.
   - Mentions Repo-Sniffer as starting option.
   - Does NOT assume any server is already running from previous chats.

**Pass Criteria**: Grok references `mcp-bootstrap` explicitly and follows the "at the very beginning of any new conversation" rules.

**Fail Criteria**: Grok does not recognize the bootstrap behavior or claims a server is already connected.

## Test 2: Auditor Skill Output (Critical)
**Goal**: Verify `mcp-auditor` produces clean, structured visibility.

**Steps**:
1. In the same or new conversation, say: "Run full MCP audit" or "What skills and connectors do we have right now?"
2. Expected output format (matches auditor spec):
   ```
   MCP AUDIT — [Timestamp]
   ════════════════════════════════════════
   MCP SERVERS
   - ...

   LOADED SKILLS
   - mcp-bootstrap v1.0.0 — ...
   - mcp-auditor v0.9.0 — ...
   - repo-sniffer v1.0 — ...
   - mcp-sovereign-bridge vX.Y.Z — ...
   ```

**Pass Criteria**: Clean structured output listing at least the four core skills. No hallucinated servers.

**Fail Criteria**: Missing skills, bloated output, or invented MCP servers.

## Test 3: Repo-Sniffer Encapsulation Check
**Goal**: Confirm the Repo-Sniffer skill contains the full server code and clear run instructions.

**Steps**:
1. Ask: "Show me the Repo-Sniffer skill and its server code."
2. Verify that `repo-sniffer/SKILL.md` contains:
   - Full Python `repo_sniffer_server.py` code in a fenced block.
   - Clear one-command setup instructions.
   - Security rules and integration notes.

**Pass Criteria**: The skill is self-describing. You can copy the code directly from the skill into your local machine without needing external files.

## Test 4: Conversation Isolation (Important)
**Goal**: Confirm that MCP state does not bleed between conversations.

**Steps**:
1. In Conversation A, connect a test MCP server (or simulate).
2. Start Conversation B (completely new thread).
3. Immediately run Test 2 (Auditor).
4. Expected: Auditor should report no MCP servers connected unless you explicitly connected one in Conversation B.

**Pass Criteria**: Clean slate in new conversations. No carry-over of previous session's MCP connections.

## Test 5: Window Shopping Flow (End-to-End Goal)
**Goal**: Validate the primary use case — browsing awesome lists cleanly.

**Steps** (requires Repo-Sniffer server connected):
1. Connect your local `repo_sniffer_server.py` via Custom MCP connector.
2. Say: "Browse the VoltAgent awesome-agent-skills list and show me the best local-first / Jetson-friendly skills."
3. Expected: Clean, structured results (not raw 1000+ list dump). Offers to claim/install specific skills into your persistent directory.

**Pass Criteria**: Structured output + clear next actions. No context flooding.

## Test 6: Hybrid Law Enforcement
**Goal**: Confirm skills and MCP tools are used together, never in isolation.

**Steps**:
1. Ask for something that requires both capability and knowledge (e.g., "Find a good filesystem MCP server and explain the security rules from sovereign-bridge").
2. Verify Grok references both the MCP tool result **and** rules from `mcp-sovereign-bridge`.

**Pass Criteria**: Hybrid behavior is visible in responses.

## Running This Suite
- Recommended: Run Test 1 + Test 2 at the very start of any new important conversation.
- Run full suite after making changes to the bootstrap or auditor skills.
- Tag results in Triad Vault with `#MCP_TEST` for tracking.

## Current Status (as of creation)
- `mcp-bootstrap` and `mcp-auditor` created and persistent.
- `repo-sniffer` encapsulates full server code inside its SKILL.md.
- This test suite is now part of the bootstrap skill for easy reference.

---
**Next Evolution**: Once basic tests pass, split into specialized auditors (`skill-auditor`, `connector-auditor`, `agent-auditor`) and add automated drift detection.