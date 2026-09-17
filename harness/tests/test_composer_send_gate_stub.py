"""Offline documentation test for the Gemini Spark composer send gate.

This is deliberately a logic-only stub.  It does not attach to a browser,
resolve a selector, submit a message, or contact Spark.  The one-character
threshold records the smallest contract that a future UI adapter must verify:
the Send control becomes clickable once the composer contains one character.
"""

from __future__ import annotations

import unittest


def send_clickable(composer_text: str) -> bool:
    """Model Spark's send gate without performing a send."""

    return len(composer_text) >= 1


class ComposerSendGateStubTests(unittest.TestCase):
    """Document the offline composer-state transition."""

    def test_send_is_not_clickable_before_first_character(self) -> None:
        self.assertFalse(send_clickable(""))

    def test_send_becomes_clickable_after_one_character(self) -> None:
        self.assertTrue(send_clickable("x"))

    def test_send_remains_clickable_after_the_threshold(self) -> None:
        self.assertTrue(send_clickable("xy"))


if __name__ == "__main__":
    unittest.main()
