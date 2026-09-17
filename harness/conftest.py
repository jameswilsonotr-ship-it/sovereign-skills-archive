"""Pytest fixtures for the offline phone MCP harness."""

import pytest

from .phone_mcp import OfflinePhoneMCP


@pytest.fixture
def phone_mcp() -> OfflinePhoneMCP:
    """Return a SPEC-002 stub with side effects denied."""

    return OfflinePhoneMCP()


@pytest.fixture
def simulated_phone_mcp() -> OfflinePhoneMCP:
    """Return a fully in-memory stub for testing explicit opt-in behavior."""

    return OfflinePhoneMCP(allow_side_effects=True)


@pytest.fixture
def assert_default_denied():
    """Assert the standard denial envelope for a side-effecting intent."""

    def _assert(response: dict) -> None:
        assert response["ok"] is False
        assert response["mode"] == "offline"
        assert response["error"]["code"] == "DEFAULT_DENY"

    return _assert
