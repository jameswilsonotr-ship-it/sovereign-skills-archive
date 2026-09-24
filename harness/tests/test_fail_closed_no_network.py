"""Regression tests for the harness' offline network policy.

The guard is deliberately installed by an autouse fixture so a fixture under
test cannot accidentally reach the network during setup or teardown.  The
test below exercises each socket-creation and name-resolution entry point
without ever opening a real socket.
"""

import socket

import pytest


class NetworkAccessAttempt(AssertionError):
    """Raised whenever test code attempts to use a network entry point."""


def _deny_network(*args, **kwargs):
    raise NetworkAccessAttempt("network access is disabled in the harness")


_NETWORK_ENTRY_POINTS = (
    "socket",
    "create_connection",
    "create_server",
    "socketpair",
    "fromfd",
    "fromshare",
    "dup",
    "getaddrinfo",
    "gethostbyname",
    "gethostbyname_ex",
    "getnameinfo",
)


@pytest.fixture(autouse=True)
def fail_closed_network(monkeypatch):
    """Make every test in this module fail closed before touching the network."""

    for entry_point in _NETWORK_ENTRY_POINTS:
        monkeypatch.setattr(socket, entry_point, _deny_network, raising=False)

    yield


def test_network_entry_points_fail_closed():
    """Socket creation and hostname resolution are rejected deterministically."""

    attempts = (
        lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        lambda: socket.create_connection(("example.invalid", 443), timeout=0),
        lambda: socket.create_server(("127.0.0.1", 0)),
        lambda: socket.socketpair(),
        lambda: socket.getaddrinfo("example.invalid", 443),
        lambda: socket.gethostbyname("example.invalid"),
        lambda: socket.gethostbyname_ex("example.invalid"),
        lambda: socket.getnameinfo(("127.0.0.1", 443), 0),
    )

    for attempt in attempts:
        with pytest.raises(NetworkAccessAttempt, match="network access is disabled"):
            attempt()
