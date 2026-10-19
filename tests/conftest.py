from __future__ import annotations

import socket

import pytest


@pytest.fixture(autouse=True)
def deny_live_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make an accidental real socket attempt fail every test immediately."""

    def fail_socket(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline tests must not open live sockets")

    monkeypatch.setattr(socket, "socket", fail_socket)

