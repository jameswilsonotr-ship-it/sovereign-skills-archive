import os
import logging
from typing import Optional, List, Dict, Any
from sovereign_engine.core.models import (
    VaultState, ResearchPassPayload, AuditReport, PullRequest, NavigationLog, ConstraintProfile
)
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.sensors.module_1_agnostic import execute_agnostic_pass
from sovereign_engine.sensors.module_2_constrained import execute_constrained_pass
from sovereign_engine.floor.module_0_deconfliction import ForestFloorDeconflictor
from sovereign_engine.audit.module_4_adversarial_auditor import AdversarialAuditor
from sovereign_engine.curation.module_5_git_curator import GitFlowCurator
from sovereign_engine.navigator.module_6_forest_navigator import ForestNavigator
from sovereign_engine.synthesis.module_3_multimodal import MultiModalSynthesizer

logger = logging.getLogger("sovereign_engine.orchestrator")


class SovereignEngine:
    """
    Sovereign Research Engine v4.0 / v1.0 Main State Machine.
    Coordinates Sensors (Modules 1/2), Floor Deconfliction (Module 0),
    Adversarial Auditing (Module 4), Git-Flow Curation (Module 5),
    Forest Navigation (Module 6), and Multi-Modal Synthesis (Module 3).
    Features Self-Healing retry loops and Self-Modulating adaptive execution.
    """

    def __init__(
        self,
        vault_root_dir: str,
        llm_client: Optional[LLMClient] = None,
        enable_adversarial_audit: bool = True,
        deconfliction_threshold: float = 0.50
    ):
        self.vault_root = os.path.abspath(vault_root_dir)
        self.llm_client = llm_client or LLMClient(provider="mock")
        self.enable_adversarial_audit = enable_adversarial_audit

        self.vault_state = VaultState()
        self.deconflictor = ForestFloorDeconflictor(similarity_threshold=deconfliction_threshold)
        self.auditor = AdversarialAuditor(auditor_client=self.llm_client)
        self.curator = GitFlowCurator(vault_root_dir=self.vault_root, client=self.llm_client)
        self.navigator = ForestNavigator(client=self.llm_client)
        self.synthesizer = MultiModalSynthesizer(client=self.llm_client)

    def run_single_pass(
        self,
        target_subject: str,
        constrained: bool = False,
        constraint_profile: Optional[ConstraintProfile] = None
    ) -> Dict[str, Any]:
        """
        Executes a complete single research pass through the full Sovereign pipeline.
        """
        logger.info(f"--- Starting Sovereign Pass for: '{target_subject}' ---")
        self.vault_state.current_target = target_subject

        # 1. Discovery Sensor Pass (Module 1 or 2)
        try:
            if constrained:
                pass_payload = execute_constrained_pass(
                    target_subject, constraint_profile, client=self.llm_client
                )
            else:
                pass_payload = execute_agnostic_pass(target_subject, client=self.llm_client)
        except Exception as e:
            logger.error(f"[Self-Healing Engine] Sensor pass failed: {e}. Retrying with agnostic fallback...")
            pass_payload = execute_agnostic_pass(target_subject, client=self.llm_client)

        # Update pending leaves in VaultState
        for leaf in pass_payload.oak_tree:
            self.vault_state.pending_leaves.append(leaf)

        # 2. Floor Deconfliction Pass (Module 0)
        resolved_terms, conflicts = self.deconflictor.deconflict_terms(
            pass_payload.glossary_delta, self.vault_state
        )
        pass_payload.glossary_delta = resolved_terms

        # 3. Adversarial Audit Pass (Module 4) - Self-Modulating Check
        audit_report = None
        if self.enable_adversarial_audit:
            audit_report = self.auditor.run_adversarial_audit(target_subject, payload_a=pass_payload)
            
            # Self-modulating adjustment based on hallucination risk score
            if audit_report.hallucination_risk_score > 7:
                logger.warning(
                    f"[Self-Modulating Audit] High hallucination risk score ({audit_report.hallucination_risk_score}). "
                    f"Flagging PR for strict human adjudication."
                )

        # 4. Git-Flow Staging & Curation Pass (Module 5)
        pr = self.curator.create_pull_request(
            payload=pass_payload,
            audit_report=audit_report,
            vault_state=self.vault_state
        )

        # 5. Multi-Modal Artifact Synthesis (Module 3)
        artifact = self.synthesizer.synthesize_artifact(pass_payload)

        # 6. Forest Navigation Pass (Module 6)
        nav_log = self.navigator.navigate_vault(self.vault_state)

        logger.info(f"--- Pass Completed for '{target_subject}'. PR: {pr.pr_id} ---")

        return {
            "pass_payload": pass_payload,
            "conflicts": conflicts,
            "audit_report": audit_report,
            "pull_request": pr,
            "artifact": artifact,
            "navigation_log": nav_log
        }

    def run_recursive_loop(self, root_target: str, max_iterations: int = 3, auto_approve: bool = False) -> List[Dict[str, Any]]:
        """
        Executes a recursive, self-navigating research loop up to max_iterations.
        Prevents researching in circles by tracking VaultState.
        """
        results = []
        current_target = root_target

        for i in range(1, max_iterations + 1):
            logger.info(f"\n=================== RECURSIVE ITERATION {i}/{max_iterations} ===================")
            step_res = self.run_single_pass(current_target)
            results.append(step_res)

            if auto_approve and step_res["pull_request"]:
                self.curator.approve_and_merge_pr(step_res["pull_request"].pr_id, self.vault_state)

            # Determine next target from Navigator directive
            nav_log: NavigationLog = step_res["navigation_log"]
            if nav_log.prioritized_targets:
                next_target_name = nav_log.prioritized_targets[0].leaf_name
            else:
                next_target_name = f"{root_target} Sub-Branch {i+1}"

            # Self-modulating check: prevent researching same target twice
            if next_target_name in [r["pass_payload"].current_target for r in results]:
                logger.info(f"[Self-Modulating Engine] Target '{next_target_name}' already researched. Picking secondary directive.")
                if len(nav_log.prioritized_targets) > 1:
                    next_target_name = nav_log.prioritized_targets[1].leaf_name
                else:
                    next_target_name = f"{root_target} Expansion Phase {i+1}"

            current_target = next_target_name

        return results
