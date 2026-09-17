from __future__ import annotations

from collections import Counter
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
CONCURRENT_CALLS = 500


def test_composio_fixture_account_ids_are_wired(
    composio_account_ids: dict[str, str | dict[str, str]],
) -> None:
    assert composio_account_ids == {
        "gmail": {
            "Otr": "gmail_illipe-eaves",
            "Liv": "gmail_deash-pungle",
            "Vesper": "gmail_algy-alpen",
        },
        "github": "github_unhex-ume",
        "linear": "linear_diver-forbow",
        "drive": "googledrive_baste-nous",
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


def test_concurrent_dummy_connector_calls_are_logged_x500(
    call_log,
    composio_account_ids: dict[str, str | dict[str, str]],
) -> None:
    account_pairs = [
        (provider, account_id)
        for provider, account_ids in composio_account_ids.items()
        for account_id in (
            account_ids.values() if isinstance(account_ids, dict) else (account_ids,)
        )
    ]
    jobs = [
        (*account_pairs[sequence % len(account_pairs)], sequence)
        for sequence in range(CONCURRENT_CALLS)
    ]

    def call(job: tuple[str, str, int]) -> dict[str, Any]:
        provider, account_id, sequence = job
        if provider == "gmail":
            connector = GmailConnector(account_id=account_id)
            return call_log.invoke(
                connector,
                "search_threads",
                query=f"fixture:{sequence}",
                limit=1,
            )
        elif provider == "github":
            connector = GithubConnector(account_id=account_id)
            return call_log.invoke(
                connector,
                "search_repositories",
                query=f"fixture:{sequence}",
                limit=1,
            )
        elif provider == "linear":
            connector = LinearConnector(account_id=account_id)
            return call_log.invoke(
                connector,
                "list_issues",
                status=f"fixture:{sequence}",
                limit=1,
            )
        connector = DriveConnector(account_id=account_id)
        return call_log.invoke(
            connector,
            "list_files",
            query=f"fixture:{sequence}",
            limit=1,
        )

    with ThreadPoolExecutor(max_workers=64) as executor:
        responses = list(executor.map(call, jobs))

    assert len(responses) == CONCURRENT_CALLS
    assert call_log.count() == CONCURRENT_CALLS
    request_tokens = {
        request["query"] if "query" in request else request["status"]
        for request in (response["request"] for response in responses)
    }
    assert request_tokens == {f"fixture:{sequence}" for sequence in range(CONCURRENT_CALLS)}
    rows = call_log.connection.execute(
        """
        SELECT connector, account_id, COUNT(*)
        FROM connector_calls
        GROUP BY connector, account_id
        ORDER BY connector, account_id
        """
    ).fetchall()
    expected_counts = Counter(
        account_pairs[index % len(account_pairs)] for index in range(CONCURRENT_CALLS)
    )
    assert Counter(
        (connector, account_id, count) for connector, account_id, count in rows
    ) == Counter(
        (provider, account_id, count)
        for (provider, account_id), count in expected_counts.items()
    )


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
