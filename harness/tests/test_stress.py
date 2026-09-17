from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
from threading import Thread
from typing import Any

import httpx
import pytest
from pydantic import ValidationError

from sovereign_harness.connectors import (
    DriveConnector,
    GithubConnector,
    GmailConnector,
    LinearConnector,
)
from sovereign_harness.phone_mcp import PhoneRequestHandler

pytestmark = pytest.mark.stress

ACCOUNT_BOUND_CONNECTORS = (
    DriveConnector,
    GithubConnector,
    LinearConnector,
    GmailConnector,
)


def test_composio_fixture_account_ids_are_wired(
    composio_account_ids: dict[str, str],
) -> None:
    assert composio_account_ids == {
        "Otr": "gmail_illipe-eaves",
        "Liv": "gmail_deash-pungle",
        "Vesper": "gmail_algy-alpen",
    }


@pytest.mark.parametrize(
    "bad_account_id",
    (
        None,
        "",
        " ",
        "\t",
        " gmail_illipe-eaves",
        "gmail_illipe-eaves ",
        "gmail/illipe-eaves",
        "gmail illipe-eaves",
        "\x00gmail_illipe-eaves",
        0,
        object(),
        ["gmail_illipe-eaves"],
    ),
    ids=(
        "none",
        "empty",
        "space",
        "tab",
        "leading-whitespace",
        "trailing-whitespace",
        "slash",
        "embedded-space",
        "control-character",
        "integer",
        "object",
        "list",
    ),
)
def test_malformed_account_ids_are_rejected(
    bad_account_id: Any,
) -> None:
    for connector in ACCOUNT_BOUND_CONNECTORS:
        with pytest.raises(ValidationError):
            connector(account_id=bad_account_id)


def test_concurrent_dummy_connector_calls_are_logged(call_log, composio_account_ids) -> None:
    jobs = [
        (account_id, sequence)
        for account_id in composio_account_ids.values()
        for sequence in range(24)
    ]

    def call(job: tuple[str, int]) -> dict[str, Any]:
        account_id, sequence = job
        connector = GmailConnector(account_id=account_id)
        return connector.search_threads(query=f"fixture:{sequence}", limit=1)

    with ThreadPoolExecutor(max_workers=12) as executor:
        responses = list(executor.map(call, jobs))

    for response in responses:
        call_log.record(response)

    assert len(responses) == 72
    assert call_log.count() == 72
    rows = call_log.connection.execute(
        """
        SELECT account_id, COUNT(*)
        FROM connector_calls
        GROUP BY account_id
        ORDER BY account_id
        """
    ).fetchall()
    assert rows == [
        ("gmail_algy-alpen", 24),
        ("gmail_deash-pungle", 24),
        ("gmail_illipe-eaves", 24),
    ]


def test_phone_health_handles_concurrent_offline_load() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), PhoneRequestHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/health"

        def get_health(_: int) -> tuple[int, str]:
            response = httpx.get(url, timeout=5.0)
            return response.status_code, response.json()["service"]

        with ThreadPoolExecutor(max_workers=16) as executor:
            responses = list(executor.map(get_health, range(128)))

        assert responses == [(200, "phone-bridge")] * 128
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
