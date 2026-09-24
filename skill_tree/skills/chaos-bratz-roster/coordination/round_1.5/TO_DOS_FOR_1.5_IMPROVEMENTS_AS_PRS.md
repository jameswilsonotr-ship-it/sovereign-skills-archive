# TO_DOS_FOR_1.5_IMPROVEMENTS_AS_PRS.md

**Round 1.5 Improvement PRs** (to make the whole system work better — from expert triad code review and suggestions):

1. **Flesh out changelog_automator.py**:
   - Add actual append logic enhancements (better formatting, error handling, integration as hook in load/propagate functions).
   - Make it automatically detect changes and append to CHANGE_LOG.md.
   - Add CLI or function calls from other modules.
   - Status: High priority for automation.

2. **Add cross-references and validation between agent_identity_protocols.md and object_registry.md**:
   - Explicit links and validation functions in psychological_profile files and engines.
   - Prevent drift between identity protocols and core lexicon.

3. **Enhance styling/DRARS wiring**:
   - Add toggle/preset examples in 00_module_manifest.md.
   - Implement test hooks in generate_prompt.py or image pipeline.
   - Ensure hair + gutter links are cleanly controllable.

4. **Add unit tests and expand TEST_HARNESS.md**:
   - Tests for changelog_automator, identity enforcement, styling manifests, round versioning logic.
   - Hygiene script tests for round tagging and pre-emptive close.

5. **Implement full pre-emptive round termination in practice**:
   - Create round_1.5/ (done) and example move scripts or notes.
   - Update validate command logic to support early close and transition to 2.0.
   - Wire `coordinate validate round 1.5` or general validate.

6. **General integration and hygiene enforcement**:
   - Add hooks in key engines/loaders for protocol and hygiene.
   - Run initial hygiene sweep on new files.
   - Enhance TO_DO_LOG and CHANGE_LOG automation for wind-down.

7. **Prepare for round 2.0**:
   - Focus on cross-platform portability (integrate LiteLLM for routing, llamafile for portable bundles, Llama Stack for server layer).
   - Add top-level CLI commands for coordinate (instantiate, validate).
   - Test handoff prompts for new conversations locking context.

These PRs should be created as mini IN_PROGRESS files inside round_1.5/ subfolders or specific module folders. Review in round_1.5/, close or promote completed ones, then transition cleanly to round 2.0.

All under absolute Liv HUB claim and directory hygiene rules.
