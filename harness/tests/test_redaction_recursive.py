"""Offline contract tests for recursively redacting nested PII payloads.

The redactor here is deliberately a small test stub.  It models the boundary
that an online redaction service would expose while keeping this harness
deterministic and network-free.
"""

from __future__ import annotations

import copy
import unittest
from collections.abc import Mapping
from typing import Any


REDACTED = "[REDACTED]"
PII_KEYS = frozenset(
    {
        "address",
        "dob",
        "email",
        "full_name",
        "name",
        "phone",
        "ssn",
    }
)


def _normalise_key(key: object) -> str:
    """Return a case-insensitive, separator-independent field name."""

    return str(key).casefold().replace("-", "_").replace(" ", "_")


def offline_redaction_stub(value: Any, *, field_name: object | None = None) -> Any:
    """Recursively redact values held by known PII fields.

    This is intentionally a test-only stand-in for a remote PII redaction
    service.  It returns new containers and leaves unknown fields unchanged.
    """

    if field_name is not None and _normalise_key(field_name) in PII_KEYS:
        return REDACTED

    if isinstance(value, Mapping):
        return {
            key: offline_redaction_stub(item, field_name=key)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [offline_redaction_stub(item) for item in value]

    if isinstance(value, tuple):
        return tuple(offline_redaction_stub(item) for item in value)

    return value


class TestRecursiveOfflineRedaction(unittest.TestCase):
    """Exercise the nested-payload contract without external services."""

    def test_redacts_pii_across_nested_mappings_and_lists(self) -> None:
        payload = {
            "request_id": "req-001",
            "profile": {
                "name": "Ada Example",
                "email": "ada@example.test",
                "contacts": [
                    {"phone": "+1-202-555-0100", "label": "primary"},
                    {"email": "backup@example.test", "label": "backup"},
                ],
            },
            "events": [
                {
                    "actor": {"ssn": "000-12-3456"},
                    "message": "consent recorded",
                }
            ],
        }

        redacted = offline_redaction_stub(payload)

        self.assertEqual(redacted["request_id"], "req-001")
        self.assertEqual(redacted["profile"]["name"], REDACTED)
        self.assertEqual(redacted["profile"]["email"], REDACTED)
        self.assertEqual(redacted["profile"]["contacts"][0]["phone"], REDACTED)
        self.assertEqual(redacted["profile"]["contacts"][0]["label"], "primary")
        self.assertEqual(redacted["profile"]["contacts"][1]["email"], REDACTED)
        self.assertEqual(redacted["events"][0]["actor"]["ssn"], REDACTED)
        self.assertEqual(redacted["events"][0]["message"], "consent recorded")

    def test_recurses_through_tuples_and_normalises_field_names(self) -> None:
        payload = (
            {"FULL-NAME": "Grace Example", "safe": 7},
            [{"phone": "+1-202-555-0111"}, {"address": "1 Example Way"}],
        )

        redacted = offline_redaction_stub(payload)

        self.assertIsInstance(redacted, tuple)
        self.assertEqual(redacted[0]["FULL-NAME"], REDACTED)
        self.assertEqual(redacted[0]["safe"], 7)
        self.assertEqual(redacted[1][0]["phone"], REDACTED)
        self.assertEqual(redacted[1][1]["address"], REDACTED)

    def test_does_not_mutate_the_original_payload(self) -> None:
        payload = {
            "user": {"email": "user@example.test"},
            "history": [{"phone": "+1-202-555-0122"}],
        }
        original = copy.deepcopy(payload)

        redacted = offline_redaction_stub(payload)

        self.assertEqual(payload, original)
        self.assertIsNot(redacted, payload)
        self.assertEqual(payload["user"]["email"], "user@example.test")
        self.assertEqual(redacted["user"]["email"], REDACTED)

    def test_preserves_scalars_empty_containers_and_unknown_fields(self) -> None:
        payload = {
            "none_value": None,
            "count": 0,
            "enabled": False,
            "empty_list": [],
            "empty_dict": {},
            "notes": "not PII",
        }

        redacted = offline_redaction_stub(payload)

        self.assertEqual(redacted, payload)
        self.assertIsNot(redacted["empty_list"], payload["empty_list"])
        self.assertIsNot(redacted["empty_dict"], payload["empty_dict"])


if __name__ == "__main__":
    unittest.main()
