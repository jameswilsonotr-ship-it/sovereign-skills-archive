from __future__ import annotations

from string import ascii_letters, digits
from typing import Any

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from sovereign_harness.connectors import (
    AccountBoundConnector,
    DriveConnector,
    GithubConnector,
    GmailConnector,
    ImageConnector,
    LinearConnector,
    WebConnector,
)

pytestmark = [pytest.mark.property, pytest.mark.smoke]

ACCOUNT_BOUND_CONNECTORS: tuple[type[AccountBoundConnector], ...] = (
    DriveConnector,
    GithubConnector,
    LinearConnector,
    GmailConnector,
)
ACCOUNT_ID_FIRST_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
ACCOUNT_ID_CHARS = ACCOUNT_ID_FIRST_CHARS + "._-"
INVALID_ACCOUNT_ID_CHARS = " /\\:@\t\n\x00😀"
QUERY_CHARS = ascii_letters + digits + " ._:/-"
PATH_CHARS = ascii_letters + digits + "._-"


@st.composite
def valid_account_ids(draw: st.DrawFn) -> str:
    first = draw(st.sampled_from(ACCOUNT_ID_FIRST_CHARS))
    suffix = draw(st.text(alphabet=ACCOUNT_ID_CHARS, max_size=127))
    return first + suffix


@st.composite
def malformed_account_id_strings(draw: st.DrawFn) -> str:
    valid = valid_account_ids()
    invalid_character = st.sampled_from(INVALID_ACCOUNT_ID_CHARS)
    return draw(
        st.one_of(
            st.just(""),
            st.just(" "),
            st.tuples(valid, invalid_character).map(lambda parts: "".join(parts)),
            st.tuples(invalid_character, valid).map(lambda parts: "".join(parts)),
            st.text(alphabet=ACCOUNT_ID_CHARS, min_size=129, max_size=160),
            st.tuples(valid, st.just(" ")).map(lambda parts: "".join(parts)),
        )
    )


def fixture_queries() -> st.SearchStrategy[str]:
    """Generate bounded query values suitable for every offline search stub."""

    return st.text(alphabet=QUERY_CHARS, min_size=1, max_size=64)


def fixture_limits() -> st.SearchStrategy[int]:
    """Generate the bounded page sizes accepted by offline connector calls."""

    return st.integers(min_value=0, max_value=100)


def fixture_paths() -> st.SearchStrategy[str]:
    """Generate URL paths without introducing characters needing URL escaping."""

    return st.text(alphabet=PATH_CHARS, min_size=1, max_size=32)


def optional_fixture_styles() -> st.SearchStrategy[str | None]:
    """Generate both omitted and explicit style values for image fixtures."""

    return st.one_of(st.none(), fixture_queries())


@pytest.mark.parametrize("connector", ACCOUNT_BOUND_CONNECTORS)
@settings(max_examples=100, deadline=None)
@given(account_id=valid_account_ids())
def test_account_id_fuzz_accepts_only_the_documented_alphabet(
    connector: type[AccountBoundConnector],
    account_id: str,
) -> None:
    instance = connector(account_id=account_id)

    assert instance.account_id == account_id
    assert instance._reply("property_probe")["account_id"] == account_id


@pytest.mark.parametrize("connector", ACCOUNT_BOUND_CONNECTORS)
@settings(max_examples=100, deadline=None)
@given(account_id=malformed_account_id_strings())
def test_account_id_fuzz_rejects_malformed_strings(
    connector: type[AccountBoundConnector],
    account_id: str,
) -> None:
    with pytest.raises(ValidationError, match="account_id"):
        connector(account_id=account_id)


@pytest.mark.parametrize("connector", ACCOUNT_BOUND_CONNECTORS)
@settings(max_examples=25, deadline=None)
@given(
    account_id=st.one_of(
        st.none(),
        st.integers(),
        st.binary(),
        st.lists(st.text(max_size=8), max_size=3),
    )
)
def test_account_id_fuzz_rejects_non_strings(
    connector: type[AccountBoundConnector],
    account_id: Any,
) -> None:
    with pytest.raises(ValidationError):
        connector(account_id=account_id)


@settings(max_examples=100, deadline=None)
@given(account_id=valid_account_ids())
def test_valid_account_ids_are_stable_at_the_128_character_boundary(
    account_id: str,
) -> None:
    if len(account_id) < 128:
        account_id = account_id + "a" * (128 - len(account_id))

    assert len(account_id) == 128
    for connector in ACCOUNT_BOUND_CONNECTORS:
        assert connector(account_id=account_id).account_id == account_id


@given(
    prefix=st.text(alphabet=ACCOUNT_ID_CHARS, min_size=128, max_size=128),
)
def test_account_ids_longer_than_128_characters_are_rejected(prefix: str) -> None:
    with pytest.raises(ValidationError, match="invalid characters"):
        DriveConnector(account_id=prefix + "a")


@pytest.mark.parametrize("connector", ACCOUNT_BOUND_CONNECTORS)
@settings(max_examples=40, deadline=None)
@given(
    account_id=valid_account_ids(),
    query=fixture_queries(),
    limit=fixture_limits(),
)
def test_account_bound_search_requests_round_trip_generated_values(
    connector: type[AccountBoundConnector],
    account_id: str,
    query: str,
    limit: int,
) -> None:
    instance = connector(account_id=account_id)
    if connector is LinearConnector:
        response = instance.list_issues(status=query, limit=limit)
    elif connector is DriveConnector:
        response = instance.list_files(query=query, limit=limit)
    elif connector is GithubConnector:
        response = instance.search_repositories(query=query, limit=limit)
    else:
        response = instance.search_threads(query=query, limit=limit)

    request = response["request"]
    assert (request["query"] if "query" in request else request["status"]) == query
    assert request["limit"] == limit


@settings(max_examples=40, deadline=None)
@given(query=fixture_queries(), style=optional_fixture_styles())
def test_image_fixture_preserves_generated_prompt_and_style(
    query: str,
    style: str | None,
) -> None:
    response = ImageConnector().render(prompt=query, style=style)

    assert response["request"] == {"prompt": query, "style": style}
    assert response["data"]["source"] == "offline-fixture"


@settings(max_examples=40, deadline=None)
@given(path=fixture_paths())
def test_web_fixture_normalizes_generated_paths_without_network(path: str) -> None:
    response = WebConnector().fetch(url=f"https://example.invalid/{path}")

    assert response["request"]["url"] == f"https://example.invalid/{path}"
    assert response["data"]["source"] == "offline-fixture"
