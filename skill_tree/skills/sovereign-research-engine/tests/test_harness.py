import os
import sys
import time
import json
import tempfile
import logging
from typing import Dict, Any

from sovereign_engine.orchestrator import SovereignEngine
from sovereign_engine.core.models import ResearchPassPayload, AuditReport, ConstraintProfile, GlossaryTerm
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.floor.module_0_deconfliction import ForestFloorDeconflictor
from sovereign_engine.curation.module_5_git_curator import MarkdownRenderer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("sovereign_test_harness")


class SovereignTestHarness:
    """
    Comprehensive Test Harness & Scenario Simulator for Sovereign Research Engine.
    Validates self-healing schema resilience, self-modulating loop convergence,
    adversarial audit divergence detection, and vault filesystem integrity.
    """

    def __init__(self):
        self.results: Dict[str, Any] = {}

    def run_all_scenarios(self) -> bool:
        logger.info("=====================================================================")
        logger.info("  STARTING SOVEREIGN RESEARCH ENGINE TEST HARNESS SCENARIO SUITE    ")
        logger.info("=====================================================================")

        start_time = time.time()
        success = True

        scenarios = [
            ("Scenario 1: Self-Healing LLM Schema Repair", self._test_self_healing_schema),
            ("Scenario 2: Deconfliction & Semantic Clone Clustering", self._test_deconfliction_clustering),
            ("Scenario 3: Adversarial Peer Audit & Hallucination Scoring", self._test_adversarial_audit),
            ("Scenario 4: Markdown Rendering & Frontmatter Formatting", self._test_markdown_rendering),
            ("Scenario 5: Multi-Turn Recursive Loop & Vault Staging", self._test_recursive_vault_staging),
            ("Scenario 6: Obsidian Canvas JSON Structure Validation", self._test_obsidian_canvas_export)
        ]

        for name, test_func in scenarios:
            logger.info(f"\n---> Executing {name}...")
            t0 = time.time()
            try:
                test_func()
                elapsed = time.time() - t0
                logger.info(f"✔ {name} PASSED in {elapsed:.3f}s")
                self.results[name] = {"status": "PASSED", "duration": round(elapsed, 3)}
            except Exception as e:
                elapsed = time.time() - t0
                logger.error(f"❌ {name} FAILED in {elapsed:.3f}s: {e}")
                self.results[name] = {"status": "FAILED", "error": str(e), "duration": round(elapsed, 3)}
                success = False

        total_elapsed = time.time() - start_time
        logger.info("\n=====================================================================")
        logger.info(f"  TEST HARNESS COMPLETED IN {total_elapsed:.3f}s - SUCCESS: {success} ")
        logger.info("=====================================================================")

        return success

    def _test_self_healing_schema(self):
        """Verifies that the LLM client handles invalid JSON/schema and retries/recovers."""
        client = LLMClient(provider="mock")
        # Generate with invalid JSON prompt expectation
        payload = client.generate_structured(
            prompt="CRITICAL FORCE REPAIR TEST",
            system_prompt="Return malformed data initially",
            response_model=ResearchPassPayload,
            max_retries=3
        )
        assert payload is not None
        assert payload.current_target is not None

    def _test_deconfliction_clustering(self):
        """Verifies hybrid TF-IDF + lexical deconfliction on near-duplicate jargon."""
        deconflictor = ForestFloorDeconflictor(similarity_threshold=0.50)
        from sovereign_engine.core.models import VaultState

        vault = VaultState()
        term_a = GlossaryTerm(term="Sovereign Node", canonical_definition="Autonomous computing unit executing offline models.")
        term_b = GlossaryTerm(term="Sovereign Cluster", canonical_definition="Autonomous computing unit executing offline models.")

        deconflictor.deconflict_terms([term_a], vault)
        terms, conflicts = deconflictor.deconflict_terms([term_b], vault)

        assert len(conflicts) == 1
        assert conflicts[0]["existing_term"] == "Sovereign Node"

    def _test_adversarial_audit(self):
        """Verifies adversarial peer review pass generation and risk scoring."""
        from sovereign_engine.audit import AdversarialAuditor
        auditor = AdversarialAuditor()
        report = auditor.run_adversarial_audit("Sovereign Edge Computing")
        assert report.hallucination_risk_score >= 1
        assert len(report.compared_models) == 2
        assert "WINNING" in report.final_adjudication or "STAND-OFF" in report.final_adjudication

    def _test_markdown_rendering(self):
        """Verifies rendering of Pydantic payloads into frontmatter-rich Markdown."""
        client = LLMClient(provider="mock")
        payload = client.generate_structured("TARGET: Test Markdown", "System", ResearchPassPayload)
        md = MarkdownRenderer.render_research_pass(payload)
        
        assert "---" in md
        assert "subject: Test Markdown" in md
        assert "### 1. SOTA TAXONOMY" in md
        assert "### 6. GLOSSARY DELTA" in md

    def _test_recursive_vault_staging(self):
        """Simulates 3-pass recursive loop and verifies file movements in /INCOMING/ and /CANONICAL/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = SovereignEngine(vault_root_dir=tmpdir)
            loop_res = engine.run_recursive_loop("Recursive Test Root", max_iterations=2, auto_approve=True)
            assert len(loop_res) == 2
            
            incoming_files = os.listdir(engine.curator.incoming_dir)
            canonical_files = os.listdir(engine.curator.nodes_dir)
            
            assert len(incoming_files) == 2
            assert len(canonical_files) == 2

    def _test_obsidian_canvas_export(self):
        """Validates generation of valid Obsidian .canvas JSON graph structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = SovereignEngine(vault_root_dir=tmpdir)
            engine.run_single_pass("Canvas Test")
            canvas = engine.deconflictor.export_obsidian_canvas(engine.vault_state)
            
            assert "nodes" in canvas
            assert "edges" in canvas
            assert len(canvas["nodes"]) > 0


if __name__ == "__main__":
    harness = SovereignTestHarness()
    success = harness.run_all_scenarios()
    sys.exit(0 if success else 1)
