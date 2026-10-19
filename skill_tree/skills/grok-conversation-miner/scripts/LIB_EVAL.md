# Library evaluation — 2026-09-11 03:41 EDT

Code execution sandbox has **no outbound pip**. Install attempts are expected to fail. Patterns only unless stdlib.

| Candidate | Present? | Verdict |
|---|---|---|
| tarfile + hashlib + json + email.message + zoneinfo + pathlib | YES | **SSoT packer / stamps / mail-fs** |
| pytest / unittest | YES (both) | **Smoke runner** |
| PyYAML | YES | stamps; not required |
| python-dateutil | YES | unused; isoformat enough |
| jsonschema | NO | schema-lite in census.validate_row |
| python-frontmatter | NO | yaml_stamp_block in gcm_lib |
| conversation-tk / queelius/ctk | NO / no pip | Pattern: per-conv space + jsonl export + zip import. Do not swallow. L8 cousin. |
| risaacr/claude-chats | NO | Pattern: parse export → sqlite → markdown. L8 cousin. |
| Owlock/easy-grok-chat-exporter | NO | Pattern: grok → md/txt/jsonl. Recon only. |
| skill-orchestrator package_skills | local skill | Preferred packer when packaging skills |

Do not vendor a fifth mouth. Export is recon. Lake remains Drive-first via keep-lake-query.
