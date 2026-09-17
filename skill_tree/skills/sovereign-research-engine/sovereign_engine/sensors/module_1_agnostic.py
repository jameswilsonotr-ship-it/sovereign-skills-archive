import logging
from typing import Optional
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.core.models import ResearchPassPayload

logger = logging.getLogger("sovereign_engine.sensors.module_1")

AGNOSTIC_SYSTEM_PROMPT = """
ROLE: You are a Graduate-Level Research Examiner and Systems Analyst. You will
receive a TARGET SUBJECT. Treat this as a post-doctoral technical review.
Define nothing basic.

CITATION RULE: NEVER use markdown hyperlink syntax [text](url) and NEVER dump
a bibliography at the end. Every citation MUST be inline, plain-text:
[Source: Name — https://full-url.com (Year)]. If unverifiable, state
[UNVERIFIED SPECULATION].

EXECUTE THE FOLLOWING IN ORDER:
1. SOTA TAXONOMY: Map the current state-of-the-art players, frameworks, or physical realities governing this TARGET.
2. CLAIM AUDIT: If the payload contains prior assumptions, ruthlessly flag anything outdated, hallucinated, or superseded.
3. THE BLIND SPOTS: Name 3-5 critical tier-1 elements, competing theories, or supply-chain realities a competent practitioner would expect here that are currently missing.
4. DECISION TREE: Identify 3 major fork-points or bottlenecks within this TARGET.
   - IF [Condition/Choice] THEN [Ramification]
   - MITIGATION / ALTERNATIVE: [Concrete workaround]
5. THE OAK TREE (Leaf Generation): Deconstruct this TARGET into a hierarchical map for future deep-dive research passes:
   - Forest: [Broad Domain]
   - Tree: [Major Branch]
   - Branch: [Specific Sub-Category]
   - Leaf: [A single, laser-focused topic requiring its own dedicated prompt] — [1 sentence on why it matters]
6. GLOSSARY DELTA (mandatory, do not skip): List every load-bearing term, named product, or protocol you introduced or relied on in this response that a future pass would need defined.
"""


def execute_agnostic_pass(target_subject: str, client: Optional[LLMClient] = None) -> ResearchPassPayload:
    """Executes a Level 1 Agnostic Research Pass (Module 1)."""
    if client is None:
        client = LLMClient(provider="mock")
    
    logger.info(f"Executing Module 1 Agnostic Pass on TARGET: '{target_subject}'")
    user_prompt = f"TARGET SUBJECT: {target_subject}"
    
    payload = client.generate_structured(
        prompt=user_prompt,
        system_prompt=AGNOSTIC_SYSTEM_PROMPT,
        response_model=ResearchPassPayload
    )
    payload.pass_type = "AGNOSTIC"
    return payload
