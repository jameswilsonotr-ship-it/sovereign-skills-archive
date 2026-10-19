# Sovereign Research Engine (v4.0 / v1.0 Architecture)

[![CI/CD Pipeline](https://github.com/sovereign-engine/sovereign/actions/workflows/ci.yml/badge.svg)](https://github.com/sovereign-engine/sovereign/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An enterprise-grade, local-first, autonomous technical discovery and curation engine. Built around strict Pydantic schema enforcement, LangGraph-inspired state machine orchestration, hybrid TF-IDF + lexical deconfliction, multi-model adversarial peer review, and Git-flow human-in-the-loop staging for Obsidian vaults.

---

## 🏛 System Architecture Overview

The Sovereign Engine operates as a recursive, self-cleaning knowledge graph pipeline:

```
                          ┌──────────────────────────┐
                          │  Module 6: Navigator     │
                          │ (Gap Analysis/Recursive) │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │  Modules 1 & 2: Sensors  │
                          │ (Agnostic / Constrained) │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │ Module 0: Forest Floor   │
                          │ (Hybrid Deconfliction)   │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │ Module 4: Peer Auditor   │
                          │ (Async Divergence Audit) │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │  Module 5: Git Curator   │
                          │  (/INCOMING/ -> PR Staging│
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │ Module 3: Multi-Modal    │
                          │ (Audio Briefs/Mind-Maps) │
                          └──────────────────────────┘
```

---

## 🧩 Core Modules

| Module | Name | Function / Description |
| :--- | :--- | :--- |
| **Module 1** | **Agnostic Research Sensor** | Post-doctoral Level 1 technical discovery pass generating SOTA taxonomy, claim audits, blind spots, decision trees, Oak Tree leaves, and glossary deltas. |
| **Module 2** | **Constrained Research Sensor** | Principal Edge-Systems pass evaluating technical viability against strict network, hardware, thermal, and power boundaries. |
| **Module 0** | **The Forest Floor (Soil-Sync)** | Hybrid lexical + TF-IDF semantic deconfliction engine. Merges synonymous jargon, detects semantic clones, updates dual-layer (ELI5 + Technical) definitions, and exports Obsidian `.canvas` graphs. |
| **Module 4** | **Adversarial Auditor** | Async peer-review engine pitting Model A against Model B to identify technical divergence, verify inline plain-text citations, assign hallucination risk scores (1-10), and declare adjudication. |
| **Module 5** | **Git-Flow Curator** | Human-in-the-loop staging area. Renders frontmatter-rich Markdown notes into `/INCOMING/<pr_id>/`, generates structured PR change logs, and handles canonical merging into `/CANONICAL/nodes/`. |
| **Module 6** | **Forest Navigator** | Executive orchestration function. Performs vault gap analysis, staleness audits (>30 days), recursive target ranking (Critical, Expansion, Curation), and target bloat checks. |
| **Module 3** | **Multi-Modal Synthesizer** | Transforms canonical research into 5-minute dual-person audio scripts (Architect + Novice), Mermaid.js visual mind-maps, and spaced-repetition flashcards. |

---

## ⚡ Self-Healing & Self-Modulating Features

- **Self-Healing Schema Resilience**: Automatically intercepts JSON parsing and Pydantic validation failures. Retries with schema error correction prompts and falls back gracefully to schema-compliant default objects to guarantee uninterrupted pipeline execution.
- **Self-Modulating Loop Execution**:
  - Automatically modulates audit rigor based on hallucination risk scores (scores > 7 trigger mandatory human adjudication flags).
  - Dynamically detects duplicate research directives during recursive loops and switches to secondary prioritized leaves to prevent searching in circles.
  - Automatically audits note staleness and flags outdated canonical definitions for re-passes.

---

## 🚀 Quick Start & CLI Usage

### Installation

```bash
git clone https://github.com/sovereign-engine/sovereign.git
cd sovereign
pip install pydantic pyyaml rich
```

### Running Commands

```bash
# 1. Execute a single Agnostic Research Pass
python sovereign_engine/cli/main.py run --target "Edge LLM Quantization" --vault-dir ./my_vault

# 2. Execute a Constrained Research Pass (Module 2)
python sovereign_engine/cli/main.py run --target "Edge LLM Quantization" --constrained --vault-dir ./my_vault

# 3. Trigger a Recursive Research Loop (3 iterations)
python sovereign_engine/cli/main.py loop --target "Autonomous Sovereign AI" --iterations 3 --auto-approve --vault-dir ./my_vault

# 4. Export Obsidian Canvas (.canvas JSON)
python sovereign_engine/cli/main.py canvas --vault-dir ./my_vault --output vault_graph.canvas

# 5. Run Standalone Smoke Test
python sovereign_engine/cli/main.py smoke
```

---

## 🧪 Testing Suite & Test Harness

The codebase includes 100% passing unit tests, standalone smoke tests, and an advanced scenario test harness.

```bash
# Run Unit Tests
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py"

# Run Standalone Smoke Test
PYTHONPATH=. python3 tests/smoke_test.py

# Run Test Harness Scenario Suite
PYTHONPATH=. python3 tests/test_harness.py
```

---

## 📂 Vault Directory Layout

```
sovereign_vault/
├── INCOMING/
│   └── pass_20260808_210040_15f1aa/
│       ├── PR.md                                  # Human-in-the-loop Pull Request
│       └── Edge_LLM_Quantization.md               # Incoming frontmatter-rich note
└── CANONICAL/
    ├── nodes/
    │   └── Edge_LLM_Quantization.md               # Merged canonical note
    └── glossary.md                                # Master deconflicted glossary
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
