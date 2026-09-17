"""Dependency-free contract test for the offline health response."""

import json
import unittest


class OfflineHealthStub:
    """In-memory stand-in for ``GET /health``; it performs no I/O."""

    def get(self, path: str) -> dict[str, str]:
        if path != "/health":
            raise ValueError(f"unsupported stub path: {path}")
        return {"status": "ok", "version": "offline"}


class TestHealthShape(unittest.TestCase):
    def test_health_json_contains_only_status_and_version(self) -> None:
        payload = OfflineHealthStub().get("/health")

        self.assertEqual(set(payload), {"status", "version"})
        self.assertEqual(payload["status"], "ok")
        self.assertIsInstance(payload["version"], str)
        self.assertTrue(payload["version"])
        self.assertEqual(json.loads(json.dumps(payload)), payload)

