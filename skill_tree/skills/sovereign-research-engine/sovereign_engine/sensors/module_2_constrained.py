import logging
from typing import Optional
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.core.models import ResearchPassPayload, ConstraintProfile

logger = logging.getLogger("sovereign_engine.sensors.module_2")

CONSTRAINED_SYSTEM_PROMPT = """
ROLE: You are a Principal Edge-Systems Architect and Risk Officer. You will
receive a TARGET SUBJECT and a CONSTRAINT PROFILE (strict physical/network boundaries).

CITATION RULE: Inline plain-text URLs only: [Source: Name — https://full-url.com (Year)]. No markdown links. No end-of-page bibliographies.

EXECUTE THE FOLLOWING IN ORDER:
1. CONSTRAINT AUDIT: Evaluate the TARGET strictly against the provided CONSTRAINT PROFILE. Will this technology break under the specified network, hardware, or thermal limits?
2. SOTA TAXONOMY: Map the current state-of-the-art frameworks addressing this TARGET that survive the stated constraints.
3. THE BLIND SPOTS: Name 3 tier-1 alternatives or failure modes the payload completely overlooks regarding these specific limitations.
4. SURVIVABILITY DECISION TREE: Identify 3 catastrophic failure cascades natively inherent to this TARGET under the provided constraints.
   - IF [Hardware/Network Failure] THEN [Ramification]
   - MITIGATION: [Concrete edge-native workaround]
5. THE OAK TREE (Leaf Generation): Deconstruct this TARGET into a hierarchical map for future deep-dives.
6. GLOSSARY DELTA (mandatory): List every load-bearing term, named product, or protocol introduced.
"""


def execute_constrained_pass(
    target_subject: str,
    constraint_profile: Optional[ConstraintProfile] = None,
    client: Optional[LLMClient] = None
) -> ResearchPassPayload:
    """Executes a Level 1 Constrained Research Pass (Module 2)."""
    if client is None:
        client = LLMClient(provider="mock")
    if constraint_profile is None:
        constraint_profile = ConstraintProfile()

    logger.info(f"Executing Module 2 Constrained Pass on TARGET: '{target_subject}'")
    
    user_prompt = f"""
TARGET SUBJECT: {target_subject}
CONSTRAINT PROFILE:
- Network Limits: {constraint_profile.network_limits}
- Hardware Limits: {constraint_profile.hardware_limits}
- Thermal Limits: {constraint_profile.thermal_limits}
- Power Limits: {constraint_profile.power_limits}
"""

    payload = client.generate_structured(
        prompt=user_prompt,
        system_prompt=CONSTRAINED_SYSTEM_PROMPT,
        response_model=ResearchPassPayload
    )
    payload.pass_type = "CONSTRAINED"
    return payload
