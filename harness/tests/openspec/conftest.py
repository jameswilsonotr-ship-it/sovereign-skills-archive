from __future__ import annotations

import os
import socket

import pytest

from harness.openspec_stubs import StubHarness, UnimplementedHarness


@pytest.fixture(autouse=True)
def network_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make an accidental network dependency fail the test immediately."""

    def blocked(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("OpenSpec harness is offline-only")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)


@pytest.fixture
def sut() -> StubHarness | UnimplementedHarness:
    """Use the stub backend by default; select the red phase with an env var."""

    if os.environ.get("OPENSPEC_SUT") == "unimplemented":
        return UnimplementedHarness()
    return StubHarness()
