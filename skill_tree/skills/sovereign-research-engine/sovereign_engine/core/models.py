from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TermStatus(str, Enum):
    NEW = "new"
    CONFLICTING = "conflicting"
    SUPERSEDED = "superseded"
    CANONICAL = "canonical"


class GlossaryTerm(BaseModel):
    term: str = Field(..., description="Load-bearing term or named concept")
    status: TermStatus = Field(default=TermStatus.NEW, description="Status of the term")
    canonical_definition: str = Field(..., description="One-sentence canonical definition")
    conflicts_with: Optional[str] = Field(default="none", description="Prior term or 'none'")
    eli5_definition: Optional[str] = Field(default=None, description="Simplified ELI5 explanation")
    technical_definition: Optional[str] = Field(default=None, description="In-depth technical definition")
    source_pass_id: Optional[str] = Field(default=None, description="Pass ID or Model ID that introduced this")


class OakTreeLeaf(BaseModel):
    forest: str = Field(..., description="Broad Domain")
    tree: str = Field(..., description="Major Branch")
    branch: str = Field(..., description="Specific Sub-Category")
    leaf: str = Field(..., description="A single laser-focused topic requiring dedicated prompt")
    rationale: str = Field(..., description="One sentence on why it matters")
    researched: bool = Field(default=False, description="Whether this leaf has been researched")
    priority: str = Field(default="MEDIUM", description="Priority level: HIGH, MEDIUM, LOW")


class ForkPoint(BaseModel):
    condition: str = Field(..., description="Condition or Choice (IF ...)")
    ramification: str = Field(..., description="Ramification (THEN ...)")
    mitigation: str = Field(..., description="Concrete workaround or alternative")


class BlindSpot(BaseModel):
    name: str = Field(..., description="Missing element, competing theory, or reality")
    description: str = Field(..., description="Explanation of why this blind spot matters")
    severity: str = Field(default="HIGH", description="Severity level")


class ConstraintProfile(BaseModel):
    network_limits: Optional[str] = Field(default="100 Mbps, intermittent latency", description="Network boundaries")
    hardware_limits: Optional[str] = Field(default="8GB RAM, 4 CPU cores, no dedicated GPU", description="Hardware boundaries")
    thermal_limits: Optional[str] = Field(default="Passive cooling, 45C max ambient", description="Thermal boundaries")
    power_limits: Optional[str] = Field(default="15W TDP max", description="Power boundaries")


class ResearchPassPayload(BaseModel):
    engine_id: str = Field(..., description="Model or engine identifier")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    current_target: str = Field(..., description="Restated target subject")
    pass_type: str = Field(default="AGNOSTIC", description="Pass type: AGNOSTIC or CONSTRAINED")
    sota_taxonomy: List[str] = Field(default_factory=list, description="Current state-of-the-art players/frameworks")
    claim_audits: List[str] = Field(default_factory=list, description="Audit of prior assumptions/claims")
    blind_spots: List[BlindSpot] = Field(default_factory=list, description="3-5 critical tier-1 missing elements")
    decision_tree: List[ForkPoint] = Field(default_factory=list, description="Major fork-points or bottlenecks")
    oak_tree: List[OakTreeLeaf] = Field(default_factory=list, description="Deconstructed hierarchical research leaves")
    glossary_delta: List[GlossaryTerm] = Field(default_factory=list, description="Terms introduced in this pass")
    constraint_audit: Optional[List[str]] = Field(default=None, description="Evaluation against constraint profile")


class DivergenceClaim(BaseModel):
    claim_a: str = Field(..., description="Claim from Model A")
    claim_b: str = Field(..., description="Claim from Model B")
    stakes: str = Field(..., description="Why this contradiction matters")


class CitationVerification(BaseModel):
    url: str = Field(..., description="Inline citation URL")
    source_name: str = Field(..., description="Source name")
    is_verified: bool = Field(default=True, description="Whether source is reputable and valid")
    notes: str = Field(default="", description="Verification notes")


class AuditReport(BaseModel):
    engine_id: str = Field(..., description="Auditor model name")
    audit_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    compared_models: List[str] = Field(..., description="e.g. ['Gemini 1.5 Pro', 'Claude 3.5 Sonnet']")
    consensus_map: List[str] = Field(default_factory=list, description="Ground truth where models agree")
    divergence_report: List[DivergenceClaim] = Field(default_factory=list, description="Hard contradictions")
    citation_verifications: List[CitationVerification] = Field(default_factory=list, description="Spot check on citations")
    hallucination_risk_score: int = Field(..., description="Score 1-10")
    final_adjudication: str = Field(..., description="WINNING CLAIM or STAND-OFF")
    winning_claim: Optional[str] = Field(default=None, description="Details of winning claim if applicable")


class PullRequest(BaseModel):
    engine_id: str = Field(..., description="Curator model identifier")
    pr_id: str = Field(..., description="PR Unique Identifier or Timestamp")
    status: str = Field(default="PENDING HUMAN REVIEW", description="PR Status")
    summary_of_changes: str = Field(..., description="3-sentence summary of research additions")
    diff_additions: List[str] = Field(default_factory=list, description="New leaves or terms")
    diff_modifications: List[str] = Field(default_factory=list, description="Modified canonical definitions")
    diff_conflicts: List[str] = Field(default_factory=list, description="Technical contradictions")
    checklist_approved: bool = Field(default=False, description="Human approval flag")
    checklist_rejected: bool = Field(default=False, description="Human rejection flag")
    checklist_partial: Optional[List[str]] = Field(default=None, description="Partial acceptance list")
    checklist_adjudicate: Optional[str] = Field(default=None, description="Human adjudication choice")
    merge_instructions: str = Field(..., description="Exact folder path movements")
    lineage_log: str = Field(..., description="Research lineage log")


class PrioritizedTarget(BaseModel):
    target_type: str = Field(..., description="CRITICAL, EXPANSION, or CURATION")
    leaf_name: str = Field(..., description="Leaf or task name")
    reason: str = Field(..., description="Prioritization rationale")


class NavigationLog(BaseModel):
    engine_id: str = Field(..., description="Navigator model identifier")
    navigation_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    vault_health_pct: float = Field(..., description="Percentage of Oak Tree completed")
    high_priority_leaves: List[str] = Field(default_factory=list, description="Leaves bridging knowledge gaps")
    redundant_targets: List[str] = Field(default_factory=list, description="Flagged redundant targets")
    stale_notes: List[str] = Field(default_factory=list, description="Notes crossing stale threshold")
    prioritized_targets: List[PrioritizedTarget] = Field(default_factory=list, description="Top 3 ranked research targets")
    woods_check: str = Field(..., description="Evaluation if research direction is bloated")
    next_directive_payload: str = Field(..., description="Exact target payload for next pass")


class MultiModalArtifact(BaseModel):
    engine_id: str = Field(..., description="Model identifier")
    artifact_type: str = Field(..., description="Mind-Map, Audio Briefing, or Flashcards")
    audio_script: Optional[str] = Field(default=None, description="Dual-layer script (Architect + Novice)")
    mermaid_mindmap: Optional[str] = Field(default=None, description="Mermaid.js mind-map block")
    flashcards: Optional[List[Dict[str, str]]] = Field(default=None, description="Front/Back flashcard pairs")


class VaultState(BaseModel):
    current_target: str = Field(default="", description="Current research target")
    canonical_vault_map: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Note title -> metadata")
    pending_leaves: List[OakTreeLeaf] = Field(default_factory=list, description="Unresearched leaves")
    glossary_db: Dict[str, GlossaryTerm] = Field(default_factory=dict, description="Term -> GlossaryTerm")
    pr_queue: List[PullRequest] = Field(default_factory=list, description="Pending Pull Requests")
    navigation_history: List[NavigationLog] = Field(default_factory=list, description="History of navigator logs")
    stale_data_threshold_days: int = Field(default=30, description="Staleness threshold in days")
