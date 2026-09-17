# Spark / Vesper on Gemini

Spark is the Vesper persona served through Google AI Studio and the Gemini
API. Spark is not a CMV Gmail workflow and is not a Cursor runtime. The
persona address is `vesper.mae.blackwell@gmail.com`; the supplied Composio
account ID is `gmail_algy-alpen`.

## Boundary

```text
Tier A Gemma on Pixel -> Tier B approved Vultr endpoint
                                      |
                                      v
                         Tier C Gemini API / AI Studio
                                      |
                                      v
                         Spark / Vesper response
```

Use Tier C only when the routing policy says the request may leave the
device/VPS boundary, or when Spark/Vesper is explicitly requested. Do not
silently send a Tier A prompt to Gemini because a local runner is slow.

## AI Studio project setup

Create or select a dedicated Google AI Studio project owned by the operator.
Record the project ID and approved model in the secret/config registry, not in
this repository.

1. Open <https://aistudio.google.com/>.
2. Create or select the mesh/Spark project.
3. Enable the Gemini API for that project.
4. Create an API key with the narrowest available restrictions. Prefer a
   server-side secret manager or deployment secret over a developer shell
   file.
5. Set the runtime's secret reference, for example:

   ```text
   GEMINI_API_KEY=<secret-manager-reference>
   GEMINI_PROJECT_ID=<secret-manager-reference>
   GEMINI_MODEL=<approved-model-name>
   VESPER_SYSTEM_PROMPT_REF=<versioned-prompt-reference>
   ```

   The values above are variable names and placeholders only. Do not commit
   a key, a `AIza...` value, or a real secret-manager export.
6. Restrict outbound access and model selection at the service boundary. A
   local developer can use AI Studio's prompt UI for a manual test, but
   production-shaped calls go through the explicitly configured Gemini API
   client.

The API key is for the Gemini API project. It is not a Gmail password, a
Composio token, or a Tailscale key. Rotate it independently and redact it
from request/exception logs.

## System prompt pointer

The prompt is a versioned configuration artifact, not an inline string in
the bridge template. Set `VESPER_SYSTEM_PROMPT_REF` to the approved prompt
record in the deployment secret/config registry and record its digest in the
MIS ticket.

For the prompt envelope and repository conventions, start with:

- [`SYSTEM_PROMPT_ENVELOPE_SNIPPET.md`](../skill_tree/skills/format-bible/references/SYSTEM_PROMPT_ENVELOPE_SNIPPET.md)
- [`Vesper alignment handoff`](../skill_tree/skills/system-roadmap/references/skills/vesper-alignment/handoff_2026-08-27_pose-pause-and-bus-loop.md)

Those pointers provide repository context; they are not a license to paste
secrets, Gmail content, or an unreviewed prompt into a phone or VPS image. If
a canonical Vesper prompt registry is established later, update
`VESPER_SYSTEM_PROMPT_REF` and this pointer in the same MIS change.

## Request envelope

The Spark adapter should receive an explicit envelope:

```json
{
  "persona": "vesper",
  "account_id": "gmail_algy-alpen",
  "tier": "gemini-api",
  "system_prompt_ref": "secret://prompts/vesper/<version>",
  "model": "<approved-model-name>",
  "input": "<approved, redacted request>",
  "allowed_tools": []
}
```

`account_id` is an identity selector, not a credential. The adapter must
reject `CMV`, CMV Gmail addresses, unknown persona/account combinations, and
requests that omit a system-prompt reference.

## When to escalate Gemma → Gemini

Start on the lowest permitted tier:

| Condition | Action |
| --- | --- |
| Short, non-sensitive text; local runner healthy; model fits memory | Use Tier A Gemma. |
| Local runner fails, context is too large, or bounded concurrency is needed | Use Tier B if the request's data policy permits the VPS. |
| Spark/Vesper persona is explicitly requested, or approved multimodal/reasoning capability is unavailable in A/B | Use Tier C Gemini. |
| Request contains credentials, unredacted private mail, or data not approved for Google processing | Refuse or ask for redaction; do not escalate automatically. |
| Gemini key, project, model, or prompt reference is missing | Return a configuration error; never guess or fall back to CMV. |

Every escalation records only the decision metadata needed for operations:
`request_id`, `from_tier`, `to_tier`, reason code, model ID, latency, and
redacted error class. Raw prompts and generated private content remain under
the applicable retention policy.

## AI Studio → GHA/APK handoff

The existing phone-tap launcher documents the GitHub-connected AI Studio Apps
path:

[`ai-studio-launcher/MODULE.md`](../skill_tree/skills/olivia-dev-alpha/references/integrations/ai-studio-launcher/MODULE.md)

The existing APK hygiene report documents the binary boundary:

[`apk-hygiene-sub/REPORT.md`](../skill_tree/skills/olivia-dev-alpha/references/sync_state_2026-08-06/coding-sub-driver-2026-08-13/apk-hygiene-sub-2026-08-13/REPORT.md)

Use that path to generate/test an Android artifact when needed, but keep
`*.apk`, `*.aab`, and large build archives outside Git. AI Studio/GHA is a
build or handoff path; it must not become the mesh's runtime inference
control plane.

## Minimal acceptance test

With a disposable test prompt and a non-production key:

1. Confirm the selected project/model and `VESPER_SYSTEM_PROMPT_REF`.
2. Confirm the adapter sends one Gemini API request and receives a response.
3. Confirm logs contain no API key, Gmail credential, raw prompt, or raw
   response.
4. Disable Gemini access and confirm the adapter returns a clear Tier C
   unavailable result rather than routing through CMV.
5. Record the redacted result and prompt digest in the MIS ticket.
