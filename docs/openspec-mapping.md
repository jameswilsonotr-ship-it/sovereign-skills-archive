# OpenSpec mapping

## SPEC-001 status

This checkout does not contain a `SPEC-001` document or an OpenSpec change
folder. A repository search found no `SPEC-001`, `SPEC_001`, or `openspec`
artifact outside unrelated historical references in the archived skill tree.
Therefore this PR does not claim conformance to SPEC-001 or invent
requirements that are not available locally.

When SPEC-001 is added to the repository, replace this status with links to
the exact requirement headings and update the table below. Keep the mapping
requirement-led rather than treating filenames as proof of compliance.

## Change inventory awaiting normative references

| Change area | Implementation / evidence | SPEC-001 reference |
| --- | --- | --- |
| Local OpenAI-compatible request path | `coder/client.py`, `tests/test_client.py` | Pending SPEC-001 |
| Conversation and memory boundary | `coder/chat.py`, `coder/memory.py`, `tests/test_chat.py` | Pending SPEC-001 |
| CLI behavior | `coder/cli.py`, `tests/test_cli.py` | Pending SPEC-001 |
| Offline verification | `httpx.MockTransport` in the test suite | Pending SPEC-001 |
| Local Ollama deployment shape | `docker-compose.yml`, `Dockerfile.coder` | Pending SPEC-001 |

## Reconciliation checklist

1. Add or locate the canonical SPEC-001 file and preserve its path in this
   document.
2. Map each applicable requirement to code and a deterministic offline test.
3. Record any requirement that depends on a live Ollama daemon separately from
   the offline test suite.
4. Mark requirements as satisfied, partial, or blocked with an explanation;
   do not convert a missing reference into a passing result.

