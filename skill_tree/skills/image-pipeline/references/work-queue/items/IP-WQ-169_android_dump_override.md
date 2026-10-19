# IP-WQ-169 — ANDROID mute vs dump

**Status:** OPEN  
**Owner:** image-pipeline  
**Created:** 2026-09-10 19:52 CDT

## Problem
IP-WQ-102 / ANDROID_SHOW_PATH forbids `render_file` and Imagine component tags because they serialized as brown prose on this phone (shots 133235/133236). Split-engine dump route and agentify RUNBOOK require `render_file` on kept JPEGs. IPQ-079 calls zero tags a SHOW FAIL.

2026-09-10 agentify pair followed the mute lock. Operator saw Drive links only and said emit failed.

## Proposed ladder
1. Always generate + keep + Drive triple. That does not change.
2. If operator says dump / show / inline / emit / see the pictures → `render_file` on kept JPEGs anyway. Consecutive tags = carousel i of N.
3. If tags brown-out, Drive view link is the rescue, said out loud, not the only copy on a dump turn.
4. `render_generated_image` stays demoted as the *only* copy. Legal as wrapper next to a kept file (agentify SKILL IPQ-010), never instead of the lake.

Video emit is not this ticket. That is IP-WQ-161 / 165. This chat toolset stills; Imagine-tab video is a different pipe.

Implement pairing: IP-WQ-170 writes this ladder into RENDER_ROUTE_LOCK + RUNBOOK and adds the contact-sheet rescue. 169 stays the policy; 170 is the ship.
