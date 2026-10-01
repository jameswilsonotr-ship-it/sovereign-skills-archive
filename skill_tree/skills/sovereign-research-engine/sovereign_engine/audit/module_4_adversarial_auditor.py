import asyncio
import logging
from typing import Optional, List, Tuple
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.core.models import ResearchPassPayload, AuditReport

logger = logging.getLogger("sovereign_engine.audit.module_4")

AUDITOR_SYSTEM_PROMPT = """
ROLE: You are the Lead Peer Reviewer and Forensic Systems Analyst. Your goal is
to identify "Technical Divergence" between two independent research outputs.

EXECUTE THE FOLLOWING IN ORDER:
1. CONSENSUS MAP: Identify the "Ground Truth" where both models agree.
2. DIVERGENCE REPORT: Identify "Hard Contradictions" where the models provide different technical data, protocols, or limitations.
   - CLAIM A: [What Model A said]
   - CLAIM B: [What Model B said]
   - THE STAKES: Why does this contradiction matter for the Sovereign Vault?
3. CITATION VERIFICATION: Perform a "Spot Check" on the inline citations.
   - If Model A provides a URL that Model B does not (or vice versa), evaluate if the source is reputable.
   - Flag any "Unverified Speculation" or dead links as potential hallucinations.
4. HALLUCINATION RISK SCORE: Assign a score (1-10) for this research pass.
   - 1-3: High Consensus, verifiable sources.
   - 4-7: Moderate drift, conflicting minor details.
   - 8-10: Critical contradictions on load-bearing facts; do not merge.
5. FINAL ADJUDICATION: Based on the "SOTA Taxonomy" and "Constraint Profile," which claim is technically superior?
   - If a winner is clear, state: "WINNING CLAIM: [A/B] due to [Reasoning]."
   - If a tie, state: "STAND-OFF: Requires Module 5 Human Adjudication."
"""


class AdversarialAuditor:
    """
    Module 4: Adversarial Auditor (Peer Review Engine).
    Executes cross-examination between Model A and Model B research passes.
    Supports asynchronous concurrent generation for latency reduction.
    """

    def __init__(self, client_a: Optional[LLMClient] = None, client_b: Optional[LLMClient] = None, auditor_client: Optional[LLMClient] = None):
        self.client_a = client_a or LLMClient(provider="mock", model_name="Gemini-1.5-Pro")
        self.client_b = client_b or LLMClient(provider="mock", model_name="Claude-3.5-Sonnet")
        self.auditor_client = auditor_client or LLMClient(provider="mock", model_name="Sovereign-Auditor-Adjudicator")

    def run_adversarial_audit(
        self,
        target_subject: str,
        payload_a: Optional[ResearchPassPayload] = None,
        payload_b: Optional[ResearchPassPayload] = None
    ) -> AuditReport:
        """
        Runs an adversarial audit over payload_a and payload_b for target_subject.
        If payloads are not provided, generates them concurrently via Model A and Model B.
        """
        if payload_a is None:
            logger.info(f"Generating Research Pass via Model A ({self.client_a.model_name})...")
            payload_a = self.client_a.generate_structured(
                prompt=f"TARGET SUBJECT: {target_subject}",
                system_prompt="Execute Agnostic Research Pass",
                response_model=ResearchPassPayload
            )

        if payload_b is None:
            logger.info(f"Generating Research Pass via Model B ({self.client_b.model_name})...")
            payload_b = self.client_b.generate_structured(
                prompt=f"TARGET SUBJECT: {target_subject}",
                system_prompt="Execute Agnostic Research Pass",
                response_model=ResearchPassPayload
            )

        auditor_prompt = f"""
TARGET SUBJECT: {target_subject}

--- MODEL A OUTPUT ({payload_a.engine_id}) ---
Target: {payload_a.current_target}
SOTA Taxonomy: {payload_a.sota_taxonomy}
Claim Audits: {payload_a.claim_audits}
Blind Spots: {[b.dict() for b in payload_a.blind_spots]}
Decision Tree: {[d.dict() for d in payload_a.decision_tree]}
Glossary Delta: {[g.dict() for g in payload_a.glossary_delta]}

--- MODEL B OUTPUT ({payload_b.engine_id}) ---
Target: {payload_b.current_target}
SOTA Taxonomy: {payload_b.sota_taxonomy}
Claim Audits: {payload_b.claim_audits}
Blind Spots: {[b.dict() for b in payload_b.blind_spots]}
Decision Tree: {[d.dict() for d in payload_b.decision_tree]}
Glossary Delta: {[g.dict() for g in payload_b.glossary_delta]}
"""

        logger.info(f"Running Adversarial Audit pass between {payload_a.engine_id} and {payload_b.engine_id}...")
        report = self.auditor_client.generate_structured(
            prompt=auditor_prompt,
            system_prompt=AUDITOR_SYSTEM_PROMPT,
            response_model=AuditReport
        )
        report.compared_models = [payload_a.engine_id, payload_b.engine_id]
        return report

    async def run_async_adversarial_audit(self, target_subject: str) -> AuditReport:
        """
        Asynchronously fires off Model A and Model B research passes concurrently,
        then feeds both outputs into the Adversarial Auditor pass.
        """
        loop = asyncio.get_event_loop()
        logger.info("Firing off Model A and Model B research passes concurrently via asyncio...")
        
        task_a = loop.run_in_executor(
            None,
            self.client_a.generate_structured,
            f"TARGET SUBJECT: {target_subject}",
            "Execute Agnostic Research Pass",
            ResearchPassPayload
        )
        task_b = loop.run_in_executor(
            None,
            self.client_b.generate_structured,
            f"TARGET SUBJECT: {target_subject}",
            "Execute Agnostic Research Pass",
            ResearchPassPayload
        )

        payload_a, payload_b = await asyncio.gather(task_a, task_b)
        return self.run_adversarial_audit(target_subject, payload_a, payload_b)
