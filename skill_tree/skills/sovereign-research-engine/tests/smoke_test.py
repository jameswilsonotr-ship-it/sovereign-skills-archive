import sys
import os
import tempfile
import logging

from sovereign_engine.orchestrator import SovereignEngine
from sovereign_engine.core.models import ConstraintProfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sovereign_smoke_test")


def main():
    logger.info("Starting Sovereign Research Engine Smoke Test...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = SovereignEngine(vault_root_dir=tmpdir, enable_adversarial_audit=True)
        
        # Test 1: Agnostic Single Pass
        logger.info("Running Test 1: Agnostic Pass...")
        res_agnostic = engine.run_single_pass("Sovereign Edge Computing")
        assert res_agnostic["pass_payload"] is not None
        assert res_agnostic["pull_request"] is not None
        assert res_agnostic["artifact"] is not None
        assert res_agnostic["navigation_log"] is not None
        
        # Test 2: Constrained Pass
        logger.info("Running Test 2: Constrained Pass...")
        cp = ConstraintProfile(hardware_limits="8GB RAM Jetson Orin Nano")
        res_constrained = engine.run_single_pass("Sovereign Edge Computing", constrained=True, constraint_profile=cp)
        assert res_constrained["pass_payload"].pass_type == "CONSTRAINED"
        
        # Test 3: PR Merging
        logger.info("Running Test 3: PR Approval & Merging...")
        pr_id = res_agnostic["pull_request"].pr_id
        merged = engine.curator.approve_and_merge_pr(pr_id, engine.vault_state)
        assert merged is True
        assert len(engine.vault_state.canonical_vault_map) == 1
        
        # Test 4: Recursive Loop
        logger.info("Running Test 4: Recursive Loop Execution...")
        loop_res = engine.run_recursive_loop("Autonomous AI Swarm", max_iterations=2, auto_approve=True)
        assert len(loop_res) == 2
        
    logger.info("==========================================")
    logger.info("ALL SMOKE TESTS PASSED SUCCESSFULLY! (100%)")
    logger.info("==========================================")


if __name__ == "__main__":
    main()
