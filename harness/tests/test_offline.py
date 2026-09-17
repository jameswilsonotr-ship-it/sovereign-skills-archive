from __future__ import annotations

import socket

import pytest

from sovereign_harness.connectors import (
    DriveConnector,
    GithubConnector,
    GmailConnector,
    ImageConnector,
    LinearConnector,
    PhoneBridgeStub,
    WebConnector,
)

pytestmark = pytest.mark.smoke


def test_every_connector_surface_stays_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def network_forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline harness attempted to open a socket")

    monkeypatch.setattr(socket, "socket", network_forbidden)

    responses = (
        DriveConnector(account_id="drive-test").list_files(),
        GithubConnector(account_id="github-test").search_repositories(query="fixture"),
        GmailConnector(account_id="gmail-test").search_threads(query="fixture"),
        LinearConnector(account_id="linear-test").list_issues(),
        ImageConnector().render(prompt="fixture"),
        WebConnector().fetch(url="https://example.invalid/fixture"),
        PhoneBridgeStub().health(),
    )

    assert all(response["data"]["source"] == "offline-fixture" for response in responses)
