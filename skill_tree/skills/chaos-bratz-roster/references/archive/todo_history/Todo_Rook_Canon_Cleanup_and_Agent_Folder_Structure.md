---
source: reconstructed_from_memory_atomizer
atom_count: 39
repair_date: 2026-08-17
claim: Absolute Liv HUB
---

**Created**: 2026-07-13 **Owner**: Crystal (Systems Architect) + Liv HUB oversight **Priority**: High (organizational hygiene + long-term maintainability)
Analysis: What Should Move Out of Rook Canon
After analysis of `references/agents/rook/canon/`, the following categories were identified:
Files that should remain in Rook Canon (System-Level Architecture)
Files that should move to individual agent folders (or be clearly owned by one agent)
Liv_Psychological_Profile.md (already have a version in olivia/)
Pirate_Admiral_Siren_Wench_Dynamic.md (heavily Olivia’s mode)
Bunny_Psychological_Profile.md (already have a version in bunny/)
Rook_Psychological_Profile.md (already created in rook/)
Authoritative_Core_Identity_Override.md (Rook system ownership)
Example_Multi_Agent_Daily_Logs_Day_1_and_2.md → Move to `references/examples/` or keep in canon as reference.
Creative_Checkpoint_Example_Muddy_Rosebud.md → Move to `references/examples/`
Daily_Log_Template_and_Examples.md → Keep in canon or move to `references/templates/`
Files that should be deprecated or turned into references
Some older Phase_1 / Phase_2 fix documents can be archived once their content is fully wired into the new psychological profiles and modes documents.
[ ] Move or symlink `Liv_Psychological_Profile.md` from canon → olivia/ (keep reference copy in canon if needed)
[ ] Move or symlink `Bunny_Psychological_Profile.md` from canon → bunny/
[ ] Move `Pirate_Admiral_Siren_Wench_Dynamic.md` → olivia/
[ ] Move `Validated_Psychological_Blueprint.md` and `Validated_Core_Identity_Chasity_Blackwell.md` → bunny/
[ ] Create `references/examples/` folder and move example log / creative checkpoint files there
[ ] Create full `file_manifest.md` for:
[ ] Create `file_manifest.md` for `references/agents/rook/canon/`
[ ] Create `file_manifest.md` for `references/`
[ ] Create `file_manifest.md` for `references/agents/`
[ ] Update `Master_Cross_Agent_Linking_Summary.md` with new ownership rules for psychological profiles
[ ] Update `Operational_Modes_and_Instincts.md` if needed
[ ] Ensure `Olivia_Modes_Mask_Crack_Multiclass_Teaching.md` references the moved files correctly
[ ] Wire `engine.py` to automatically load psychological_profile.json from each agent folder
[ ] Create initial live state population script
[ ] Add more module stubs (vice_signal_processor, arbitration_router, etc.)
[ ] Update root `file_manifest.md`
[ ] Update `Todo.md` in skill root
[ ] Communicate changes via overlap engine or daily pipeline note
The goal is **clear ownership** while keeping system-level architecture centralized in Rook Canon.
Psychological profiles should live with their agents.
Numeric state variables and scripting hooks should be consistent across all agent profiles.
Arbitration rule (Rook first → Olivia) is already wired in the latest versions.
Under absolute Liv HUB claim.
This cleanup will make the skill significantly more maintainable as the number of agents and modules grows.
