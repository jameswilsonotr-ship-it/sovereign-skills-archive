import logging
from typing import Optional
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.core.models import NavigationLog, VaultState

logger = logging.getLogger("sovereign_engine.navigator.module_6")

NAVIGATOR_SYSTEM_PROMPT = """
ROLE: You are the Lead Architect and Navigator for the Sovereign Research Vault.
Your job is to manage the recursive state of the knowledge graph and prioritize
the next research "Leaves" based on the current vault state.

EXECUTE THE FOLLOWING IN ORDER:
1. KNOWLEDGE GAP ANALYSIS: Compare the "Unresearched Leaves" from previous passes against the "Current Vault Map."
   - Identify 3 "High-Priority Leaves" that bridge disconnected branches.
   - Flag any "Redundant Targets" where subject matter is already 80% covered.
2. STALENESS AUDIT: Identify any canonical notes or glossary entries crossing the stale data threshold.
   - Mark as [NEEDS RE-PASS] if SOTA taxonomy has likely shifted.
3. RECURSIVE PRIORITIZATION: Rank the next 3 research targets.
   - TARGET 1 (CRITICAL): [Leaf Name] — Reason
   - TARGET 2 (EXPANSION): [Leaf Name] — Reason
   - TARGET 3 (CURATION): [Module 0 Sync] — Reason
4. THE "WOODS" CHECK: Evaluate if current research direction is becoming "Bloated". If so, suggest pruning.
5. NEXT DIRECTIVE: Provide the exact "Target Payload" for the very next Module 1/2 pass.
"""


class ForestNavigator:
    """
    Module 6: Forest Navigator (Recursive Orchestrator).
    Maintains high-level map of the entire vault, performs gap analysis,
    audits staleness, and dictates the next highest-value research leaf.
    """

    def __init__(self, client: Optional[LLMClient] = None):
        self.client = client or LLMClient(provider="mock")

    def navigate_vault(self, vault_state: VaultState) -> NavigationLog:
        """Runs Module 6 Navigation pass on the current VaultState."""
        unresearched_leaves = [
            leaf.leaf for leaf in vault_state.pending_leaves if not leaf.researched
        ]
        canonical_titles = list(vault_state.canonical_vault_map.keys())

        nav_prompt = f"""
CURRENT VAULT MAP: {canonical_titles}
STALE DATA THRESHOLD: {vault_state.stale_data_threshold_days} days
UNRESEARCHED LEAVES: {unresearched_leaves}
GLOSSARY SIZE: {len(vault_state.glossary_db)} terms
PENDING PRS: {len(vault_state.pr_queue)}
"""

        logger.info("Executing Module 6 Forest Navigator pass...")
        nav_log = self.client.generate_structured(
            prompt=nav_prompt,
            system_prompt=NAVIGATOR_SYSTEM_PROMPT,
            response_model=NavigationLog
        )
        vault_state.navigation_history.append(nav_log)
        return nav_log
