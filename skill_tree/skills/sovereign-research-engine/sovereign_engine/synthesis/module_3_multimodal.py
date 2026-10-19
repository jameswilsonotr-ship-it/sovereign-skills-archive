import logging
from typing import Optional
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.core.models import MultiModalArtifact, ResearchPassPayload

logger = logging.getLogger("sovereign_engine.synthesis.module_3")

SYNTHESIS_SYSTEM_PROMPT = """
ROLE: You are a Creative Technologist and Technical Communicator. Your goal is
to transform raw technical research into diverse end-user artifacts.

EXECUTE THE FOLLOWING IN ORDER:
1. ARTIFACT EXTRACTION: Identify the core "High-Density Facts" and "Key Decisions" from the provided notes.
2. DUAL-LAYER SCRIPTING: For audio briefs, provide a 5-minute script featuring two personas: The Architect (technical) and The Novice (ELI5).
3. TAXONOMY VISUALIZATION: Format the technical relationships into a Mermaid.js mind-map code block.
4. SPACING & REPETITION: Generate 5-10 high-quality flashcards (Front: Concept/Problem; Back: Solution/Mechanism).
"""


class MultiModalSynthesizer:
    """
    Module 3: Multi-Modal Synthesis Engine.
    Converts canonical research notes into dual-layer audio scripts,
    Mermaid.js visual mind-maps, and spaced-repetition flashcards.
    """

    def __init__(self, client: Optional[LLMClient] = None):
        self.client = client or LLMClient(provider="mock")

    def synthesize_artifact(self, payload: ResearchPassPayload) -> MultiModalArtifact:
        """Synthesizes multi-modal artifacts from a ResearchPassPayload."""
        synthesis_prompt = f"""
TARGET SUBJECT: {payload.current_target}
SOTA Taxonomy: {payload.sota_taxonomy}
Blind Spots: {[b.dict() for b in payload.blind_spots]}
Decision Tree: {[d.dict() for d in payload.decision_tree]}
Glossary Delta: {[g.dict() for g in payload.glossary_delta]}
"""
        logger.info(f"Synthesizing Module 3 Multi-Modal Artifact for '{payload.current_target}'...")
        artifact = self.client.generate_structured(
            prompt=synthesis_prompt,
            system_prompt=SYNTHESIS_SYSTEM_PROMPT,
            response_model=MultiModalArtifact
        )
        return artifact
