"""Deterministic connector call shapes.

These connectors deliberately never access a network or a provider. They make
the request contract testable while returning small, versioned fixture data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator

FIXTURES_DIR = Path(__file__).with_name("fixtures")


class CallEnvelope(BaseModel):
    """The stable result shape shared by every dummy connector."""

    connector: str
    operation: str
    account_id: str | None = None
    request: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] = Field(default_factory=dict)


class FixtureConnector(BaseModel):
    """Base for offline connectors backed by JSON fixtures."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    connector_name: ClassVar[str]
    fixture_dir: Path = FIXTURES_DIR

    def _fixture(self) -> dict[str, Any]:
        fixture_path = self.fixture_dir / f"{self.connector_name}.json"
        return json.loads(fixture_path.read_text(encoding="utf-8"))

    def _reply(self, operation: str, **request: Any) -> dict[str, Any]:
        account_id = getattr(self, "account_id", None)
        return CallEnvelope(
            connector=self.connector_name,
            operation=operation,
            account_id=account_id,
            request=request,
            data=self._fixture(),
        ).model_dump()


class AccountBoundConnector(FixtureConnector):
    """Connector base whose account identity is intentionally mandatory."""

    account_id: str

    @field_validator("account_id")
    @classmethod
    def account_id_must_be_non_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("account_id must not be empty")
        return value


class DriveConnector(AccountBoundConnector):
    connector_name = "drive"

    def list_files(
        self,
        *,
        folder_id: str | None = None,
        query: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        return self._reply(
            "list_files",
            folder_id=folder_id,
            query=query,
            limit=limit,
        )

    def get_file(self, *, file_id: str) -> dict[str, Any]:
        return self._reply("get_file", file_id=file_id)


class GithubConnector(AccountBoundConnector):
    connector_name = "github"

    def search_repositories(self, *, query: str, limit: int = 10) -> dict[str, Any]:
        return self._reply("search_repositories", query=query, limit=limit)

    def get_issue(self, *, owner: str, repo: str, number: int) -> dict[str, Any]:
        return self._reply("get_issue", owner=owner, repo=repo, number=number)

    def list_pull_requests(
        self,
        *,
        owner: str,
        repo: str,
        state: str = "open",
    ) -> dict[str, Any]:
        return self._reply("list_pull_requests", owner=owner, repo=repo, state=state)


class LinearConnector(AccountBoundConnector):
    connector_name = "linear"

    def list_issues(
        self,
        *,
        team_id: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        return self._reply(
            "list_issues",
            team_id=team_id,
            status=status,
            limit=limit,
        )

    def get_issue(self, *, identifier: str) -> dict[str, Any]:
        return self._reply("get_issue", identifier=identifier)


class GmailConnector(AccountBoundConnector):
    connector_name = "gmail"

    def search_threads(self, *, query: str, limit: int = 20) -> dict[str, Any]:
        return self._reply("search_threads", query=query, limit=limit)

    def get_thread(self, *, thread_id: str) -> dict[str, Any]:
        return self._reply("get_thread", thread_id=thread_id)


class ImageConnector(FixtureConnector):
    connector_name = "image"

    def render(self, *, prompt: str, style: str | None = None) -> dict[str, Any]:
        return self._reply("render", prompt=prompt, style=style)


class WebConnector(FixtureConnector):
    connector_name = "web"

    def fetch(self, *, url: str) -> dict[str, Any]:
        # URL parsing is useful call-shape validation; no HTTP request is made.
        normalized_url = str(httpx.URL(url))
        return self._reply("fetch", url=normalized_url)

    def search(self, *, query: str, limit: int = 10) -> dict[str, Any]:
        return self._reply("search", query=query, limit=limit)


class PhoneBridgeStub(FixtureConnector):
    """Health and fixture surface only; messaging and camera are not exposed."""

    connector_name = "phone_bridge"

    def health(self) -> dict[str, Any]:
        return self._reply("health")

    def fixture(self) -> dict[str, Any]:
        return self._reply("fixture")

    def send_sms(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError("SMS is intentionally out of scope for phone MCP v0")

    def capture_camera(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError("camera access is intentionally out of scope for phone MCP v0")


# Keep the descriptive name available to callers that want a connector-shaped API.
PhoneBridgeConnector = PhoneBridgeStub
