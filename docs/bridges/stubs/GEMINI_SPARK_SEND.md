# Gemini Spark web Send stub

Status: **non-executable design stub**  
Related contract: [SPARK_BIND](../SPARK_BIND.md) ·
[SPEC-001](../SPARK_BIND.md#spec-001-alignment) ·
[BASIC_TIER](../SPARK_BIND.md#basic_tier-alignment)

## Purpose

Describe the smallest browser automation that can prove a message was sent
from Gemini Spark's web UI. This stub deliberately does not include selectors
for a live account, credentials, browser-profile paths, or a real recipient.

## Proposed interface

```text
send_from_spark(
  session=SPARK_SESSION,
  recipient=RECIPIENT_PLACEHOLDER,
  subject=SUBJECT_PLACEHOLDER,
  body=BODY_PLACEHOLDER,
  confirm_send=true,
) -> secret_free_receipt
```

The implementation must reject `confirm_send=false` for a send operation. A
prepare-only operation may populate the form, but it must return
`prepared_not_sent` and must not call the Send control.

## Control-flow stub

```python
def send_from_spark(session, recipient, subject, body, confirm_send):
    require_operator_confirmation(confirm_send)
    page = attach_to_approved_spark_session(session)
    assert page.origin_is("gemini.google.com")
    assert page.is_spark_compose_surface()

    page.fill_recipient(recipient)
    page.fill_subject(subject)
    page.fill_body(body)

    # TODO: resolve a stable Spark UI locator at implementation time.
    send_button = page.visible_button_named("Send")
    assert send_button.is_enabled()
    send_button.click()  # Real Spark Send; never Gmail draft creation.

    result = page.wait_for_spark_sent_confirmation()
    return secret_free_receipt(result)
```

The pseudocode is intentionally incomplete. It is a contract sketch, not a
claim that these helper methods or selectors exist.

## Required guards

- **Surface guard:** stop if the current origin or compose surface is Gmail.
- **Button guard:** click only the visible Spark button whose accessible name
  is `Send`; do not submit by guessing a DOM event or invoking a Gmail API.
- **Confirmation guard:** require an operator-approved `confirm_send` value.
- **Uncertain result guard:** if the browser disconnects after the click, return
  `send_unknown` and do not retry automatically.
- **Receipt guard:** return status, timestamp, and a redacted operation ID only.
- **Secret guard:** never log page HTML, cookies, local storage, message body,
  recipient, or authentication material.

## Result vocabulary

| Result | Meaning |
| --- | --- |
| `prepared_not_sent` | Form populated; Send was not clicked. |
| `sent_confirmed` | Spark showed a post-send confirmation. |
| `send_rejected` | Spark rejected the action before delivery. |
| `send_unknown` | Connection or UI state became uncertain after the click. |
| `not_spark_surface` | The active page was not the approved Spark surface. |

`sent_confirmed` is the only successful delivery result. A Gmail draft,
queued form, or filled compose window is not equivalent.

## Verification plan

1. Use a test account and a non-sensitive recipient supplied at run time.
2. Confirm the page origin and Spark compose marker before filling fields.
3. Capture a redacted receipt after the post-send confirmation appears.
4. Test browser disconnect after click and verify `send_unknown`.
5. Test Gmail navigation and verify `not_spark_surface`.
6. Keep all live values outside the repository.
