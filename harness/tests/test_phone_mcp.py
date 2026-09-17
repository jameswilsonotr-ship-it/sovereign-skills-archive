from harness.phone_mcp import OfflinePhoneMCP


def test_health_is_read_only_and_available(phone_mcp):
    response = phone_mcp.handle_intent("health")

    assert response == {
        "ok": True,
        "intent": "health",
        "status": "ok",
        "mode": "offline",
        "spec": "SPEC-002",
        "termux": False,
        "capabilities": {
            "health": True,
            "flashlight": False,
            "sms": False,
        },
    }


def test_flashlight_is_default_deny(phone_mcp, assert_default_denied):
    response = phone_mcp.call_tool("phone_flashlight", {"action": "on"})

    assert_default_denied(response)
    assert phone_mcp.flashlight_on is False


def test_sms_is_default_deny_without_writing_outbox(phone_mcp, assert_default_denied):
    response = phone_mcp.dispatch(
        {"intent": "sms", "arguments": {"to": "+15555550123", "body": "hello"}}
    )

    assert_default_denied(response)
    assert phone_mcp.sms_outbox == ()


def test_explicit_opt_in_only_changes_in_memory_state(simulated_phone_mcp):
    flashlight = simulated_phone_mcp.handle_intent("flashlight", action="on")
    sms = simulated_phone_mcp.handle_intent(
        "sms", to="+15555550123", body="offline test"
    )

    assert flashlight["simulated"] is True
    assert flashlight["state"] == "on"
    assert sms["simulated"] is True
    assert sms["queued"] is True
    assert simulated_phone_mcp.sms_outbox == (
        {"to": "+15555550123", "body": "offline test"},
    )


def test_mcp_tool_catalog_and_aliases(phone_mcp):
    tools = phone_mcp.list_tools()

    assert [tool["name"] for tool in tools] == [
        "phone_health",
        "phone_flashlight",
        "phone_sms",
    ]
    assert phone_mcp.dispatch({"name": "phone_health"})["ok"] is True
    assert phone_mcp.dispatch({"intent": "phone.flashlight"})["error"]["code"] == (
        "DEFAULT_DENY"
    )


def test_invalid_requests_are_structured_errors(phone_mcp):
    missing_intent = phone_mcp.dispatch({})
    bad_arguments = phone_mcp.dispatch(
        {"intent": "health", "arguments": ["not", "a", "mapping"]}
    )

    assert missing_intent["error"]["code"] == "INVALID_REQUEST"
    assert bad_arguments["error"]["code"] == "INVALID_REQUEST"


def test_unknown_intent_does_not_escape_stub(phone_mcp):
    response = phone_mcp.handle_intent("camera")

    assert response["ok"] is False
    assert response["error"]["code"] == "UNKNOWN_INTENT"


def test_no_termux_dependency_is_needed():
    assert OfflinePhoneMCP.MODE == "offline"
