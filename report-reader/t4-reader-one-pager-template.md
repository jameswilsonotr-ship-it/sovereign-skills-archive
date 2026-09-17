# T4-READER — {digest_id}

**Captured:** {captured_at_utc} · **Window:** {window}  
**Reader:** T4-READER · **Tier:** INCLUDED Ultra · **Orchestration:** ORCH LADDER  
**Delivery:** offline · **On-demand:** false

## Situation

{one sentence describing the landed set, or `no landed items`.}

## Landed

| ID | Kind | Landing / status | Certainty | Owner | Source |
|---|---|---|---|---|---|
| {id} | {ca\|pr} | {title} — {status} | {certainty} | {owner} | {source_ref} |

## Mag desk

**Message:** {what matters, using only the supplied summaries}  
**Signal:** {confirmed, reported, or unknown; include the relevant IDs}  
**Line to carry:** {short audience-safe line, or `no landed items`}

## Liaison desk

**Handoff:** {who coordinates what, or `none`}  
**Open dependency:** {dependency, owner, and source ID, or `none`}  
**Unverified:** {what needs confirmation, or `none`}

## fleet desk

**Operational state:** {landed/partial/blocked summary}  
**Risk:** {source-backed risk, or `none stated`}  
**Next checkpoint:** {action, owner, and checkpoint, or `none`}

## Action queue

| Action | Owner | Source | State |
|---|---|---|---|
| {next_action} | {owner} | {id} | {open\|none\|unverified} |

> Offline local digest. No live read or write is implied. `on_demand` remains
> `false`.
