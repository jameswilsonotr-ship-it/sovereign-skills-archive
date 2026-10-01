import os
import shutil
import logging
import uuid
import yaml
from datetime import datetime
from typing import Optional, List, Dict, Any
from sovereign_engine.core.llm import LLMClient
from sovereign_engine.core.models import ResearchPassPayload, PullRequest, GlossaryTerm, VaultState, AuditReport

logger = logging.getLogger("sovereign_engine.curation.module_5")

CURATOR_SYSTEM_PROMPT = """
ROLE: You are the Git-Flow Curator. Your job is to act as the final gateway
between the /INCOMING/ research and the /CANONICAL/ Sovereign Vault. You
facilitate a "Pull Request" (PR) workflow for a human supervisor.

EXECUTE THE FOLLOWING IN ORDER:
1. SUMMARY OF CHANGES: Provide a high-level, 3-sentence summary of what this new research adds to the vault.
2. THE DIFF (Change Log): Identify specific ADDITIONS, MODIFICATIONS, and CONFLICTS.
3. HUMAN-IN-THE-LOOP CHECKLIST: Generate a Markdown task list (APPROVE, REJECT, PARTIAL, ADJUDICATE).
4. MERGE INSTRUCTIONS: Provide exact folder-path movements required (e.g. Move files from /incoming/pass_01/ to /canonical/nodes/).
5. LINEAGE LOG: State the research lineage for this PR.
"""


class MarkdownRenderer:
    """Renders Pydantic objects into frontmatter-rich Obsidian Markdown files."""

    @staticmethod
    def render_research_pass(payload: ResearchPassPayload) -> str:
        frontmatter = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "subject": payload.current_target,
            "engine_id": payload.engine_id,
            "pass_type": payload.pass_type,
            "tags": ["sovereign", payload.pass_type.lower(), "research-pass"],
            "type": "research-node"
        }

        fm_str = yaml.dump(frontmatter, sort_keys=False).strip()

        md_content = f"""---
{fm_str}
---

# RESEARCH PASS: {payload.current_target}

## ENGINE ID: {payload.engine_id}
## TIMESTAMP: {payload.timestamp}
## PASS TYPE: {payload.pass_type}

---

### 1. SOTA TAXONOMY
"""
        for item in payload.sota_taxonomy:
            md_content += f"- {item}\n"

        md_content += "\n### 2. CLAIM AUDIT\n"
        for claim in payload.claim_audits:
            md_content += f"- {claim}\n"

        md_content += "\n### 3. THE BLIND SPOTS\n"
        for spot in payload.blind_spots:
            md_content += f"- **{spot.name}** [{spot.severity}]: {spot.description}\n"

        md_content += "\n### 4. DECISION TREE\n"
        for fork in payload.decision_tree:
            md_content += f"- **IF** {fork.condition} **THEN** {fork.ramification}\n  - *MITIGATION*: {fork.mitigation}\n"

        if payload.pass_type == "CONSTRAINED" and payload.constraint_audit:
            md_content += "\n### CONSTRAINT AUDIT\n"
            for audit_item in payload.constraint_audit:
                md_content += f"- {audit_item}\n"

        md_content += "\n### 5. THE OAK TREE (Leaf Generation)\n"
        for leaf in payload.oak_tree:
            md_content += f"- **Forest**: {leaf.forest} | **Tree**: {leaf.tree} | **Branch**: {leaf.branch}\n  - **Leaf**: [[{leaf.leaf}]] — {leaf.rationale}\n"

        md_content += "\n### 6. GLOSSARY DELTA\n"
        md_content += "| Term | Status | One-Sentence Canonical Definition | Conflicts With |\n"
        md_content += "| :--- | :--- | :--- | :--- |\n"
        for term in payload.glossary_delta:
            md_content += f"| [[{term.term}]] | {term.status.value if hasattr(term.status, 'value') else term.status} | {term.canonical_definition} | {term.conflicts_with} |\n"

        return md_content

    @staticmethod
    def render_pull_request(pr: PullRequest) -> str:
        md_content = f"""---
pr_id: {pr.pr_id}
status: {pr.status}
date: {datetime.now().strftime("%Y-%m-%d")}
type: pull-request
---

# PULL REQUEST: {pr.pr_id}

## ENGINE ID: {pr.engine_id}
## STATUS: {pr.status}

### 1. SUMMARY OF CHANGES
{pr.summary_of_changes}

### 2. THE DIFF (Change Log)
**ADDITIONS**:
"""
        for add_item in pr.diff_additions:
            md_content += f"- {add_item}\n"

        md_content += "\n**MODIFICATIONS**:\n"
        for mod_item in pr.diff_modifications:
            md_content += f"- {mod_item}\n"

        md_content += "\n**CONFLICTS**:\n"
        for conf_item in pr.diff_conflicts:
            md_content += f"- {conf_item}\n"

        md_content += f"""
### 3. HUMAN-IN-THE-LOOP CHECKLIST
- [{'x' if pr.checklist_approved else ' '}] APPROVE: Merge all new Leaves and Glossary entries.
- [{'x' if pr.checklist_rejected else ' '}] REJECT: Discard this research pass.
- [{'x' if pr.checklist_partial else ' '}] PARTIAL: Accept only specific Leaves: {pr.checklist_partial or ''}
- [{'x' if pr.checklist_adjudicate else ' '}] ADJUDICATE: {pr.checklist_adjudicate or 'No conflict pending.'}

### 4. MERGE INSTRUCTIONS
{pr.merge_instructions}

### 5. LINEAGE LOG
{pr.lineage_log}
"""
        return md_content


class GitFlowCurator:
    """
    Module 5: Git-Flow Curator.
    Manages vault staging directory structure (/INCOMING/ vs /CANONICAL/).
    Generates Pull Requests for human supervisor triage.
    """

    def __init__(self, vault_root_dir: str, client: Optional[LLMClient] = None):
        self.vault_root = os.path.abspath(vault_root_dir)
        self.incoming_dir = os.path.join(self.vault_root, "INCOMING")
        self.canonical_dir = os.path.join(self.vault_root, "CANONICAL")
        self.nodes_dir = os.path.join(self.canonical_dir, "nodes")
        self.client = client or LLMClient(provider="mock")

        os.makedirs(self.incoming_dir, exist_ok=True)
        os.makedirs(self.canonical_dir, exist_ok=True)
        os.makedirs(self.nodes_dir, exist_ok=True)

    def create_pull_request(
        self,
        payload: ResearchPassPayload,
        audit_report: Optional[AuditReport] = None,
        vault_state: Optional[VaultState] = None
    ) -> PullRequest:
        """
        Stashes incoming research pass into /INCOMING/<pass_id>/ and creates a Pull Request object.
        """
        unique_suffix = uuid.uuid4().hex[:6]
        pass_id = f"pass_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_suffix}"
        pass_incoming_folder = os.path.join(self.incoming_dir, pass_id)
        os.makedirs(pass_incoming_folder, exist_ok=True)

        # Render Markdown for Research Pass
        md_text = MarkdownRenderer.render_research_pass(payload)
        pass_file_path = os.path.join(pass_incoming_folder, f"{sanitize_filename(payload.current_target)}.md")
        with open(pass_file_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        curator_prompt = f"""
INCOMING RESEARCH PASS:
Target: {payload.current_target}
Pass Type: {payload.pass_type}
Leaves: {[l.leaf for l in payload.oak_tree]}
Glossary Terms: {[g.term for g in payload.glossary_delta]}
Audit Info: {audit_report.dict() if audit_report else 'No audit pass required'}
"""
        pr = self.client.generate_structured(
            prompt=curator_prompt,
            system_prompt=CURATOR_SYSTEM_PROMPT,
            response_model=PullRequest
        )
        pr.pr_id = pass_id
        pr.merge_instructions = f"Move files from {pass_incoming_folder} to {self.nodes_dir}"

        # Save PR markdown file into /INCOMING/<pass_id>/PR.md
        pr_file_path = os.path.join(pass_incoming_folder, "PR.md")
        with open(pr_file_path, "w", encoding="utf-8") as f:
            f.write(MarkdownRenderer.render_pull_request(pr))

        if vault_state is not None:
            vault_state.pr_queue.append(pr)

        logger.info(f"Created Pull Request {pass_id} in {pass_incoming_folder}")
        return pr

    def approve_and_merge_pr(self, pr_id: str, vault_state: VaultState) -> bool:
        """
        Merges files from /INCOMING/<pr_id>/ into /CANONICAL/nodes/ and updates VaultState.
        """
        pass_incoming_folder = os.path.join(self.incoming_dir, pr_id)
        if not os.path.exists(pass_incoming_folder):
            logger.error(f"Cannot merge PR {pr_id}: Folder {pass_incoming_folder} does not exist.")
            return False

        # Move files to /CANONICAL/nodes/
        for fname in os.listdir(pass_incoming_folder):
            if fname == "PR.md":
                continue
            src = os.path.join(pass_incoming_folder, fname)
            dst = os.path.join(self.nodes_dir, fname)
            shutil.copy2(src, dst)
            logger.info(f"Merged file {fname} into {self.nodes_dir}")
            
            # Update canonical vault map
            vault_state.canonical_vault_map[fname] = {
                "title": fname.replace(".md", ""),
                "merged_at": datetime.now().isoformat(),
                "path": dst
            }

        # Update PR status in vault_state
        for pr in vault_state.pr_queue:
            if pr.pr_id == pr_id:
                pr.status = "APPROVED_AND_MERGED"
                pr.checklist_approved = True

        return True


def sanitize_filename(name: str) -> str:
    import re
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()
