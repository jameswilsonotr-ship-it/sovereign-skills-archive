from __future__ import annotations

import pytest
from pydantic import ValidationError

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


@pytest.mark.parametrize(
    "connector",
    [DriveConnector, GithubConnector, LinearConnector, GmailConnector],
)
def test_account_bound_connectors_require_account_id(connector: type[object]) -> None:
    with pytest.raises(ValidationError):
        connector()

    with pytest.raises(ValidationError):
        connector(account_id="   ")


def test_drive_call_shape_is_offline_and_account_scoped() -> None:
    response = DriveConnector(account_id="googledrive_baste-nous").list_files(
        folder_id="fixture-folder",
        query="MIS-6",
        limit=3,
    )

    assert response["connector"] == "drive"
    assert response["operation"] == "list_files"
    assert response["account_id"] == "googledrive_baste-nous"
    assert response["request"] == {
        "folder_id": "fixture-folder",
        "query": "MIS-6",
        "limit": 3,
    }
    assert response["data"]["source"] == "offline-fixture"


def test_all_provider_call_shapes_are_deterministic() -> None:
    assert GithubConnector(account_id="github_unhex-ume").get_issue(
        owner="owner", repo="repo", number=6
    )["operation"] == "get_issue"
    assert LinearConnector(account_id="linear_diver-forbow").get_issue(
        identifier="MIS-6"
    )["operation"] == "get_issue"
    assert GmailConnector(account_id="gmail_illipe-eaves").get_thread(
        thread_id="thread-1"
    )["operation"] == "get_thread"


def test_non_account_connectors_and_phone_stub_are_offline() -> None:
    assert ImageConnector().render(prompt="bunny")["data"]["source"] == "offline-fixture"
    assert WebConnector().fetch(url="https://example.invalid/mis-6")["request"] == {
        "url": "https://example.invalid/mis-6"
    }
    phone = PhoneBridgeStub().health()
    assert phone["data"]["capabilities"] == ["health", "offline-fixtures"]


def test_phone_stub_rejects_sms_and_camera() -> None:
    phone = PhoneBridgeStub()

    with pytest.raises(NotImplementedError, match="SMS"):
        phone.send_sms("555-0100", "hello")
    with pytest.raises(NotImplementedError, match="camera"):
        phone.capture_camera()
