# Sovereign Research Engine - Execution Results & Benchmarks

## Environment Metadata
- **Date**: 2026-08-08
- **Python Version**: 3.11.2
- **Pydantic Version**: 1.10.4
- **OS Platform**: Linux 6.6 x86_64
- **Workspace Path**: `/working_dir/c_22401661f0341ec3`

---

## 1. Unit Test Suite Results
- **Command**: `python3 -m unittest discover -s tests -p "test_*.py"`
- **Pass Rate**: 10 / 10 Tests Passed (100%)
- **Total Execution Time**: 0.2578s

### Unit Test Console Output
```text
..2026-08-08 21:15:56,967 [WARNING] sovereign_engine.floor.module_0: Semantic conflict detected: 'Fog Compute' vs 'Edge Compute' (score: 0.91)
.2026-08-08 21:15:56,967 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Distributed Ledger'
.2026-08-08 21:15:56,967 [INFO] sovereign_engine.sensors.module_2: Executing Module 2 Constrained Pass on TARGET: 'Distributed Ledger'
.2026-08-08 21:15:56,968 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Multi-Modal Test'
2026-08-08 21:15:56,968 [INFO] sovereign_engine.synthesis.module_3: Synthesizing Module 3 Multi-Modal Artifact for 'Multi-Modal Test'...
.2026-08-08 21:15:56,969 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model A (Gemini-1.5-Pro)...
2026-08-08 21:15:56,969 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model B (Claude-3.5-Sonnet)...
2026-08-08 21:15:56,969 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between Gemini-1.5-Pro and Claude-3.5-Sonnet...
2026-08-08 21:15:56,970 [INFO] sovereign_engine.audit.module_4: Firing off Model A and Model B research passes concurrently via asyncio...
2026-08-08 21:15:56,976 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between Gemini-1.5-Pro and Claude-3.5-Sonnet...
.2026-08-08 21:15:56,978 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Markdown Staging Test'
2026-08-08 21:15:56,979 [INFO] sovereign_engine.curation.module_5: Created Pull Request pass_20260808_211556_8667d8 in /tmp/tmprtmf7o3v/INCOMING/pass_20260808_211556_8667d8
2026-08-08 21:15:56,980 [INFO] sovereign_engine.curation.module_5: Merged file Markdown Staging Test.md into /tmp/tmprtmf7o3v/CANONICAL/nodes
.2026-08-08 21:15:56,981 [INFO] sovereign_engine.navigator.module_6: Executing Module 6 Forest Navigator pass...
.2026-08-08 21:15:56,981 [INFO] sovereign_engine.orchestrator: 
=================== RECURSIVE ITERATION 1/2 ===================
2026-08-08 21:15:56,981 [INFO] sovereign_engine.orchestrator: --- Starting Sovereign Pass for: 'Orchestrator Root Target' ---
2026-08-08 21:15:56,981 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Orchestrator Root Target'
2026-08-08 21:15:56,982 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model B (Claude-3.5-Sonnet)...
2026-08-08 21:15:56,982 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
2026-08-08 21:15:56,984 [INFO] sovereign_engine.curation.module_5: Created Pull Request pass_20260808_211556_7233aa in /tmp/tmpmu43p9k2/INCOMING/pass_20260808_211556_7233aa
2026-08-08 21:15:56,984 [INFO] sovereign_engine.synthesis.module_3: Synthesizing Module 3 Multi-Modal Artifact for 'Orchestrator Root Target'...
2026-08-08 21:15:56,984 [INFO] sovereign_engine.navigator.module_6: Executing Module 6 Forest Navigator pass...
2026-08-08 21:15:56,984 [INFO] sovereign_engine.orchestrator: --- Pass Completed for 'Orchestrator Root Target'. PR: pass_20260808_211556_7233aa ---
2026-08-08 21:15:56,985 [INFO] sovereign_engine.curation.module_5: Merged file Orchestrator Root Target.md into /tmp/tmpmu43p9k2/CANONICAL/nodes
2026-08-08 21:15:56,985 [INFO] sovereign_engine.orchestrator: 
=================== RECURSIVE ITERATION 2/2 ===================
2026-08-08 21:15:56,985 [INFO] sovereign_engine.orchestrator: --- Starting Sovereign Pass for: 'Quantization Techniques', 'Orchestrator Root Target Semantic Deduplication'] Quantization Techniques' ---
2026-08-08 21:15:56,985 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Quantization Techniques', 'Orchestrator Root Target Semantic Deduplication'] Quantization Techniques'
2026-08-08 21:15:56,986 [WARNING] sovereign_engine.floor.module_0: Semantic conflict detected: 'Quantization Techniques', 'Orchestrator Root Target Semantic Deduplication'] Quantization Techniques Node' vs 'Orchestrator Root Target Node' (score: 0.51)
2026-08-08 21:15:56,986 [INFO] sovereign_engine.floor.module_0: Exact match found for term 'Jargon Delta Sync'. Updating canonical definition.
2026-08-08 21:15:56,986 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model B (Claude-3.5-Sonnet)...
2026-08-08 21:15:56,986 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
2026-08-08 21:15:56,987 [INFO] sovereign_engine.curation.module_5: Created Pull Request pass_20260808_211556_46f6e8 in /tmp/tmpmu43p9k2/INCOMING/pass_20260808_211556_46f6e8
2026-08-08 21:15:56,988 [INFO] sovereign_engine.synthesis.module_3: Synthesizing Module 3 Multi-Modal Artifact for 'Quantization Techniques', 'Orchestrator Root Target Semantic Deduplication'] Quantization Techniques'...
2026-08-08 21:15:56,988 [INFO] sovereign_engine.navigator.module_6: Executing Module 6 Forest Navigator pass...
2026-08-08 21:15:56,988 [INFO] sovereign_engine.orchestrator: --- Pass Completed for 'Quantization Techniques', 'Orchestrator Root Target Semantic Deduplication'] Quantization Techniques'. PR: pass_20260808_211556_46f6e8 ---
2026-08-08 21:15:56,989 [INFO] sovereign_engine.curation.module_5: Merged file Quantization Techniques', 'Orchestrator Root Target Semantic Deduplication'] Quantization Techniques.md into /tmp/tmpmu43p9k2/CANONICAL/nodes
.
----------------------------------------------------------------------
Ran 10 tests in 0.024s

OK


```

---

## 2. Smoke Test Suite Results
- **Command**: `python3 tests/smoke_test.py`
- **Status**: PASSED (100%)
- **Total Execution Time**: 0.2275s

### Smoke Test Console Log
```text
INFO:sovereign_smoke_test:Starting Sovereign Research Engine Smoke Test...
INFO:sovereign_smoke_test:Running Test 1: Agnostic Pass...
INFO:sovereign_engine.orchestrator:--- Starting Sovereign Pass for: 'Sovereign Edge Computing' ---
INFO:sovereign_engine.sensors.module_1:Executing Module 1 Agnostic Pass on TARGET: 'Sovereign Edge Computing'
INFO:sovereign_engine.audit.module_4:Generating Research Pass via Model B (Claude-3.5-Sonnet)...
INFO:sovereign_engine.audit.module_4:Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
INFO:sovereign_engine.curation.module_5:Created Pull Request pass_20260808_211557_fee30e in /tmp/tmpj8ydu6vx/INCOMING/pass_20260808_211557_fee30e
INFO:sovereign_engine.synthesis.module_3:Synthesizing Module 3 Multi-Modal Artifact for 'Sovereign Edge Computing'...
INFO:sovereign_engine.navigator.module_6:Executing Module 6 Forest Navigator pass...
INFO:sovereign_engine.orchestrator:--- Pass Completed for 'Sovereign Edge Computing'. PR: pass_20260808_211557_fee30e ---
INFO:sovereign_smoke_test:Running Test 2: Constrained Pass...
INFO:sovereign_engine.orchestrator:--- Starting Sovereign Pass for: 'Sovereign Edge Computing' ---
INFO:sovereign_engine.sensors.module_2:Executing Module 2 Constrained Pass on TARGET: 'Sovereign Edge Computing'
INFO:sovereign_engine.floor.module_0:Exact match found for term 'Sovereign Edge Computing Node'. Updating canonical definition.
INFO:sovereign_engine.floor.module_0:Exact match found for term 'Jargon Delta Sync'. Updating canonical definition.
INFO:sovereign_engine.audit.module_4:Generating Research Pass via Model B (Claude-3.5-Sonnet)...
INFO:sovereign_engine.audit.module_4:Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
INFO:sovereign_engine.curation.module_5:Created Pull Request pass_20260808_211557_4f5515 in /tmp/tmpj8ydu6vx/INCOMING/pass_20260808_211557_4f5515
INFO:sovereign_engine.synthesis.module_3:Synthesizing Module 3 Multi-Modal Artifact for 'Sovereign Edge Computing'...
INFO:sovereign_engine.navigator.module_6:Executing Module 6 Forest Navigator pass...
INFO:sovereign_engine.orchestrator:--- Pass Completed for 'Sovereign Edge Computing'. PR: pass_20260808_211557_4f5515 ---
INFO:sovereign_smoke_test:Running Test 3: PR Approval & Merging...
INFO:sovereign_engine.curation.module_5:Merged file Sovereign Edge Computing.md into /tmp/tmpj8ydu6vx/CANONICAL/nodes
INFO:sovereign_smoke_test:Running Test 4: Recursive Loop Execution...
INFO:sovereign_engine.orchestrator:
=================== RECURSIVE ITERATION 1/2 ===================
INFO:sovereign_engine.orchestrator:--- Starting Sovereign Pass for: 'Autonomous AI Swarm' ---
INFO:sovereign_engine.sensors.module_1:Executing Module 1 Agnostic Pass on TARGET: 'Autonomous AI Swarm'
INFO:sovereign_engine.floor.module_0:Exact match found for term 'Jargon Delta Sync'. Updating canonical definition.
INFO:sovereign_engine.audit.module_4:Generating Research Pass via Model B (Claude-3.5-Sonnet)...
INFO:sovereign_engine.audit.module_4:Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
INFO:sovereign_engine.curation.module_5:Created Pull Request pass_20260808_211557_f0a387 in /tmp/tmpj8ydu6vx/INCOMING/pass_20260808_211557_f0a387
INFO:sovereign_engine.synthesis.module_3:Synthesizing Module 3 Multi-Modal Artifact for 'Autonomous AI Swarm'...
INFO:sovereign_engine.navigator.module_6:Executing Module 6 Forest Navigator pass...
INFO:sovereign_engine.orchestrator:--- Pass Completed for 'Autonomous AI Swarm'. PR: pass_20260808_211557_f0a387 ---
INFO:sovereign_engine.curation.module_5:Merged file Autonomous AI Swarm.md into /tmp/tmpj8ydu6vx/CANONICAL/nodes
INFO:sovereign_engine.orchestrator:
=================== RECURSIVE ITERATION 2/2 ===================
INFO:sovereign_engine.orchestrator:--- Starting Sovereign Pass for: 'Sovereign Edge Computing Quantization Techniques' ---
INFO:sovereign_engine.sensors.module_1:Executing Module 1 Agnostic Pass on TARGET: 'Sovereign Edge Computing Quantization Techniques'
WARNING:sovereign_engine.floor.module_0:Semantic conflict detected: 'Sovereign Edge Computing Quantization Techniques Node' vs 'Sovereign Edge Computing Node' (score: 0.80)
INFO:sovereign_engine.floor.module_0:Exact match found for term 'Jargon Delta Sync'. Updating canonical definition.
INFO:sovereign_engine.audit.module_4:Generating Research Pass via Model B (Claude-3.5-Sonnet)...
INFO:sovereign_engine.audit.module_4:Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
INFO:sovereign_engine.curation.module_5:Created Pull Request pass_20260808_211557_4587c8 in /tmp/tmpj8ydu6vx/INCOMING/pass_20260808_211557_4587c8
INFO:sovereign_engine.synthesis.module_3:Synthesizing Module 3 Multi-Modal Artifact for 'Sovereign Edge Computing Quantization Techniques'...
INFO:sovereign_engine.navigator.module_6:Executing Module 6 Forest Navigator pass...
INFO:sovereign_engine.orchestrator:--- Pass Completed for 'Sovereign Edge Computing Quantization Techniques'. PR: pass_20260808_211557_4587c8 ---
INFO:sovereign_engine.curation.module_5:Merged file Sovereign Edge Computing Quantization Techniques.md into /tmp/tmpj8ydu6vx/CANONICAL/nodes
INFO:sovereign_engine.orchestrator:[Self-Modulating Engine] Target 'Sovereign Edge Computing Quantization Techniques' already researched. Picking secondary directive.
INFO:sovereign_smoke_test:==========================================
INFO:sovereign_smoke_test:ALL SMOKE TESTS PASSED SUCCESSFULLY! (100%)
INFO:sovereign_smoke_test:==========================================


```

---

## 3. Test Harness 6 Scenarios Benchmark
- **Command**: `python3 tests/test_harness.py`
- **Status**: ALL 6 SCENARIOS PASSED (100%)
- **Total Execution Time**: 0.2420s

### Scenario Metrics Breakdown
1. **Scenario 1: Self-Healing LLM Schema Repair**: PASSED (<0.01s)
2. **Scenario 2: Deconfliction & Semantic Clone Clustering**: PASSED (<0.01s, Similarity Score: 0.88)
3. **Scenario 3: Adversarial Peer Audit & Hallucination Scoring**: PASSED (<0.01s, Risk Score: 2/10)
4. **Scenario 4: Markdown Rendering & Frontmatter Formatting**: PASSED (<0.01s)
5. **Scenario 5: Multi-Turn Recursive Loop & Vault Staging**: PASSED (~0.01s, 2 PRs Merged)
6. **Scenario 6: Obsidian Canvas JSON Structure Validation**: PASSED (<0.01s)

### Test Harness Console Log
```text
2026-08-08 21:15:57,433 [INFO] sovereign_test_harness: =====================================================================
2026-08-08 21:15:57,433 [INFO] sovereign_test_harness:   STARTING SOVEREIGN RESEARCH ENGINE TEST HARNESS SCENARIO SUITE    
2026-08-08 21:15:57,433 [INFO] sovereign_test_harness: =====================================================================
2026-08-08 21:15:57,433 [INFO] sovereign_test_harness: 
---> Executing Scenario 1: Self-Healing LLM Schema Repair...
2026-08-08 21:15:57,434 [INFO] sovereign_test_harness: ✔ Scenario 1: Self-Healing LLM Schema Repair PASSED in 0.001s
2026-08-08 21:15:57,434 [INFO] sovereign_test_harness: 
---> Executing Scenario 2: Deconfliction & Semantic Clone Clustering...
2026-08-08 21:15:57,434 [WARNING] sovereign_engine.floor.module_0: Semantic conflict detected: 'Sovereign Cluster' vs 'Sovereign Node' (score: 0.88)
2026-08-08 21:15:57,434 [INFO] sovereign_test_harness: ✔ Scenario 2: Deconfliction & Semantic Clone Clustering PASSED in 0.000s
2026-08-08 21:15:57,435 [INFO] sovereign_test_harness: 
---> Executing Scenario 3: Adversarial Peer Audit & Hallucination Scoring...
2026-08-08 21:15:57,435 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model A (Gemini-1.5-Pro)...
2026-08-08 21:15:57,435 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model B (Claude-3.5-Sonnet)...
2026-08-08 21:15:57,435 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between Gemini-1.5-Pro and Claude-3.5-Sonnet...
2026-08-08 21:15:57,436 [INFO] sovereign_test_harness: ✔ Scenario 3: Adversarial Peer Audit & Hallucination Scoring PASSED in 0.001s
2026-08-08 21:15:57,436 [INFO] sovereign_test_harness: 
---> Executing Scenario 4: Markdown Rendering & Frontmatter Formatting...
2026-08-08 21:15:57,437 [INFO] sovereign_test_harness: ✔ Scenario 4: Markdown Rendering & Frontmatter Formatting PASSED in 0.001s
2026-08-08 21:15:57,437 [INFO] sovereign_test_harness: 
---> Executing Scenario 5: Multi-Turn Recursive Loop & Vault Staging...
2026-08-08 21:15:57,437 [INFO] sovereign_engine.orchestrator: 
=================== RECURSIVE ITERATION 1/2 ===================
2026-08-08 21:15:57,438 [INFO] sovereign_engine.orchestrator: --- Starting Sovereign Pass for: 'Recursive Test Root' ---
2026-08-08 21:15:57,438 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Recursive Test Root'
2026-08-08 21:15:57,438 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model B (Claude-3.5-Sonnet)...
2026-08-08 21:15:57,439 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
2026-08-08 21:15:57,441 [INFO] sovereign_engine.curation.module_5: Created Pull Request pass_20260808_211557_227041 in /tmp/tmpn1bjsg2o/INCOMING/pass_20260808_211557_227041
2026-08-08 21:15:57,441 [INFO] sovereign_engine.synthesis.module_3: Synthesizing Module 3 Multi-Modal Artifact for 'Recursive Test Root'...
2026-08-08 21:15:57,441 [INFO] sovereign_engine.navigator.module_6: Executing Module 6 Forest Navigator pass...
2026-08-08 21:15:57,441 [INFO] sovereign_engine.orchestrator: --- Pass Completed for 'Recursive Test Root'. PR: pass_20260808_211557_227041 ---
2026-08-08 21:15:57,442 [INFO] sovereign_engine.curation.module_5: Merged file Recursive Test Root.md into /tmp/tmpn1bjsg2o/CANONICAL/nodes
2026-08-08 21:15:57,442 [INFO] sovereign_engine.orchestrator: 
=================== RECURSIVE ITERATION 2/2 ===================
2026-08-08 21:15:57,442 [INFO] sovereign_engine.orchestrator: --- Starting Sovereign Pass for: 'Sovereign Edge Computing Quantization Techniques' ---
2026-08-08 21:15:57,442 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Sovereign Edge Computing Quantization Techniques'
2026-08-08 21:15:57,443 [INFO] sovereign_engine.floor.module_0: Exact match found for term 'Jargon Delta Sync'. Updating canonical definition.
2026-08-08 21:15:57,443 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model B (Claude-3.5-Sonnet)...
2026-08-08 21:15:57,444 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
2026-08-08 21:15:57,445 [INFO] sovereign_engine.curation.module_5: Created Pull Request pass_20260808_211557_b7e49e in /tmp/tmpn1bjsg2o/INCOMING/pass_20260808_211557_b7e49e
2026-08-08 21:15:57,445 [INFO] sovereign_engine.synthesis.module_3: Synthesizing Module 3 Multi-Modal Artifact for 'Sovereign Edge Computing Quantization Techniques'...
2026-08-08 21:15:57,446 [INFO] sovereign_engine.navigator.module_6: Executing Module 6 Forest Navigator pass...
2026-08-08 21:15:57,446 [INFO] sovereign_engine.orchestrator: --- Pass Completed for 'Sovereign Edge Computing Quantization Techniques'. PR: pass_20260808_211557_b7e49e ---
2026-08-08 21:15:57,446 [INFO] sovereign_engine.curation.module_5: Merged file Sovereign Edge Computing Quantization Techniques.md into /tmp/tmpn1bjsg2o/CANONICAL/nodes
2026-08-08 21:15:57,446 [INFO] sovereign_engine.orchestrator: [Self-Modulating Engine] Target 'Sovereign Edge Computing Quantization Techniques' already researched. Picking secondary directive.
2026-08-08 21:15:57,447 [INFO] sovereign_test_harness: ✔ Scenario 5: Multi-Turn Recursive Loop & Vault Staging PASSED in 0.011s
2026-08-08 21:15:57,448 [INFO] sovereign_test_harness: 
---> Executing Scenario 6: Obsidian Canvas JSON Structure Validation...
2026-08-08 21:15:57,448 [INFO] sovereign_engine.orchestrator: --- Starting Sovereign Pass for: 'Canvas Test' ---
2026-08-08 21:15:57,448 [INFO] sovereign_engine.sensors.module_1: Executing Module 1 Agnostic Pass on TARGET: 'Canvas Test'
2026-08-08 21:15:57,448 [INFO] sovereign_engine.audit.module_4: Generating Research Pass via Model B (Claude-3.5-Sonnet)...
2026-08-08 21:15:57,449 [INFO] sovereign_engine.audit.module_4: Running Adversarial Audit pass between sovereign-llm-v4 and Claude-3.5-Sonnet...
2026-08-08 21:15:57,450 [INFO] sovereign_engine.curation.module_5: Created Pull Request pass_20260808_211557_7184b6 in /tmp/tmp7nyz_5um/INCOMING/pass_20260808_211557_7184b6
2026-08-08 21:15:57,450 [INFO] sovereign_engine.synthesis.module_3: Synthesizing Module 3 Multi-Modal Artifact for 'Canvas Test'...
2026-08-08 21:15:57,450 [INFO] sovereign_engine.navigator.module_6: Executing Module 6 Forest Navigator pass...
2026-08-08 21:15:57,451 [INFO] sovereign_engine.orchestrator: --- Pass Completed for 'Canvas Test'. PR: pass_20260808_211557_7184b6 ---
2026-08-08 21:15:57,451 [INFO] sovereign_test_harness: ✔ Scenario 6: Obsidian Canvas JSON Structure Validation PASSED in 0.004s
2026-08-08 21:15:57,452 [INFO] sovereign_test_harness: 
=====================================================================
2026-08-08 21:15:57,452 [INFO] sovereign_test_harness:   TEST HARNESS COMPLETED IN 0.019s - SUCCESS: True 
2026-08-08 21:15:57,452 [INFO] sovereign_test_harness: =====================================================================


```
