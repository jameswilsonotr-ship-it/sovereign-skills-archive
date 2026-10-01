from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

import duckdb
import pytest

COMPOSIO_ACCOUNT_IDS = {
    "gmail": {
        "Otr": "gmail_illipe-eaves",
        "Liv": "gmail_deash-pungle",
        "Vesper": "gmail_algy-alpen",
    },
    "github": "github_unhex-ume",
    "linear": "linear_diver-forbow",
    "drive": "googledrive_baste-nous",
}


@dataclass
class CallLog:
    """Small DuckDB ledger for connector calls made by a test."""

    connection: duckdb.DuckDBPyConnection = field(
        default_factory=lambda: duckdb.connect(database=":memory:")
    )
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def __post_init__(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE connector_calls (
                connector VARCHAR NOT NULL,
                operation VARCHAR NOT NULL,
                account_id VARCHAR,
                request_json JSON NOT NULL
            )
            """
        )

    def invoke(
        self,
        connector: Any,
        operation: str,
        **request: Any,
    ) -> dict[str, Any]:
        """Invoke a connector method and record its stable response shape."""

        response = getattr(connector, operation)(**request)
        self.record(response)
        return response

    def record(self, response: dict[str, Any]) -> None:
        """Record a connector response after an invocation completes."""

        with self._lock:
            self.connection.execute(
                """
                INSERT INTO connector_calls
                    (connector, operation, account_id, request_json)
                VALUES (?, ?, ?, ?)
                """,
                [
                    response["connector"],
                    response["operation"],
                    response["account_id"],
                    json.dumps(response["request"]),
                ],
            )

    def count(self) -> int:
        return self.connection.execute("SELECT COUNT(*) FROM connector_calls").fetchone()[0]

    def close(self) -> None:
        self.connection.close()


@pytest.fixture
def composio_account_ids() -> dict[str, str | dict[str, str]]:
    return {
        provider: dict(account_ids) if isinstance(account_ids, dict) else account_ids
        for provider, account_ids in COMPOSIO_ACCOUNT_IDS.items()
    }


@pytest.fixture
def call_log() -> Iterator[CallLog]:
    ledger = CallLog()
    try:
        yield ledger
    finally:
        ledger.close()
