import unittest
import os
import tempfile
import asyncio
from sovereign_engine.core.models import (
    GlossaryTerm, OakTreeLeaf, ResearchPassPayload, VaultState, ConstraintProfile, TermStatus
)
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.sensors import execute_agnostic_pass, execute_constrained_pass
from sovereign_engine.floor import ForestFloorDeconflictor
from sovereign_engine.audit import AdversarialAuditor
from sovereign_engine.curation import GitFlowCurator, MarkdownRenderer
from sovereign_engine.navigator import ForestNavigator
from sovereign_engine.synthesis import MultiModalSynthesizer
from sovereign_engine.orchestrator import SovereignEngine


class TestSovereignEngineModules(unittest.TestCase):

    def setUp(self):
        self.client = LLMClient(provider="mock")

    def test_core_models(self):
        term = GlossaryTerm(
            term="Edge Node",
            canonical_definition="Local compute unit."
        )
        self.assertEqual(term.term, "Edge Node")
        self.assertEqual(term.status, TermStatus.NEW)

        leaf = OakTreeLeaf(
            forest="AI", tree="Edge", branch="Inference",
            leaf="Quantization", rationale="Reduces footprint"
        )
        self.assertFalse(leaf.researched)

    def test_llm_client_self_healing(self):
        payload = self.client.generate_structured(
            prompt="TARGET: Test Subject",
            system_prompt="System Prompt",
            response_model=ResearchPassPayload
        )
        self.assertIsNotNone(payload)
        self.assertEqual(payload.current_target, "Test Subject")

    def test_module_1_agnostic(self):
        payload = execute_agnostic_pass("Distributed Ledger", client=self.client)
        self.assertEqual(payload.pass_type, "AGNOSTIC")
        self.assertGreater(len(payload.oak_tree), 0)
        self.assertGreater(len(payload.glossary_delta), 0)

    def test_module_2_constrained(self):
        cp = ConstraintProfile(hardware_limits="4GB VRAM Jetson Orin Nano")
        payload = execute_constrained_pass("Distributed Ledger", constraint_profile=cp, client=self.client)
        self.assertEqual(payload.pass_type, "CONSTRAINED")
        self.assertIsNotNone(payload.constraint_audit)

    def test_module_0_deconfliction(self):
        vault = VaultState()
        deconflictor = ForestFloorDeconflictor(similarity_threshold=0.50)

        t1 = GlossaryTerm(term="Edge Compute", canonical_definition="Localized processing node running models offline.")
        t2 = GlossaryTerm(term="Fog Compute", canonical_definition="Localized processing node running models offline.")

        deconflictor.deconflict_terms([t1], vault)
        self.assertIn("edge compute", vault.glossary_db)

        terms, conflicts = deconflictor.deconflict_terms([t2], vault)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["new_term"], "Fog Compute")

    def test_module_4_adversarial_auditor(self):
        auditor = AdversarialAuditor(auditor_client=self.client)
        report = auditor.run_adversarial_audit("Sovereign Vector Vault")
        self.assertEqual(len(report.compared_models), 2)
        self.assertGreaterEqual(report.hallucination_risk_score, 1)

        # Async test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_report = loop.run_until_complete(auditor.run_async_adversarial_audit("Async Sovereign Vault"))
        self.assertIsNotNone(async_report)
        loop.close()

    def test_module_5_curation_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            curator = GitFlowCurator(vault_root_dir=tmpdir, client=self.client)
            vault = VaultState()
            payload = execute_agnostic_pass("Markdown Staging Test", client=self.client)

            pr = curator.create_pull_request(payload, vault_state=vault)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "INCOMING", pr.pr_id)))

            merged = curator.approve_and_merge_pr(pr.pr_id, vault)
            self.assertTrue(merged)
            self.assertEqual(len(os.listdir(curator.nodes_dir)), 1)

    def test_module_6_navigator(self):
        vault = VaultState()
        nav = ForestNavigator(client=self.client)
        log = nav.navigate_vault(vault)
        self.assertIsNotNone(log.next_directive_payload)
        self.assertEqual(len(vault.navigation_history), 1)

    def test_module_3_synthesis(self):
        payload = execute_agnostic_pass("Multi-Modal Test", client=self.client)
        synth = MultiModalSynthesizer(client=self.client)
        artifact = synth.synthesize_artifact(payload)
        self.assertIsNotNone(artifact.audio_script)
        self.assertIsNotNone(artifact.mermaid_mindmap)

    def test_orchestrator_engine(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = SovereignEngine(vault_root_dir=tmpdir)
            results = engine.run_recursive_loop("Orchestrator Root Target", max_iterations=2, auto_approve=True)
            self.assertEqual(len(results), 2)
            self.assertEqual(len(engine.vault_state.canonical_vault_map), 2)


if __name__ == "__main__":
    unittest.main()
