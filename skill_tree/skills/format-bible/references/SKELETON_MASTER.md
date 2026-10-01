# Master Skeleton (sketch only — 2026-08-05)

Ordered slots for the response document template.
Implementation = FBQ-001 (not yet done).

1. OPENING_ID          (constant — formerly Opening Snake)
2. FRONT_MATTER        (fenced yaml — always)
3. SEPARATOR           (horizontal rule after front-matter)
4. INTRO_REGION        (short framing)
5. SEPARATOR           (after intro)
6. TEXT_REGION_A       (main text)
7. IMAGE_SLOT_1        (optional + own score/forensics)
8. TUI_MENU_BLOCK      (simple numbered choices when questions are asked)
9. IMAGE_SLOT_2
10. TEXT_REGION_B
11. IMAGE_SLOT_3
12. IMAGE_SLOT_4
13. FORENSICS_BLOCK    (on|off|auto — can also attach per content slot)
14. HORIZONTAL_LINE
15. METRICS            (dashboard metrics line)
16. CLOSING_ID         (constant)

Visual mode = IMAGE_SLOT_1..4 active.
TUI priority = TUI_MENU_BLOCK active and kept minimal.
Forensics flag applies at turn level and optionally under individual content slots.
