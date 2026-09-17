import json
from http.client import HTTPConnection
from threading import Thread

import pytest

from phone_service.app import create_server, health_payload
from phone_service.policy import CapabilityDenied, CapabilityPolicy, PhoneActions


def test_health_payload_is_json_safe_and_denies_sensitive_capabilities():
    payload = health_payload()

    assert payload == {
        "status": "ok",
        "service": "atomic-phone",
        "schema_version": "1",
        "capabilities": {"sms": False, "flashlight": False},
    }
    assert json.loads(json.dumps(payload)) == payload


def test_health_endpoint_returns_json_over_loopback_only():
    server = create_server(port=0)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        host, port = server.server_address
        connection = HTTPConnection(host, port, timeout=2)
        connection.request("GET", "/health?probe=offline")
        response = connection.getresponse()
        body = json.loads(response.read())
        connection.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    assert response.status == 200
    assert response.getheader("Content-Type") == "application/json"
    assert body["status"] == "ok"
    assert body["capabilities"] == {"sms": False, "flashlight": False}


@pytest.mark.parametrize(
    ("method", "args"),
    [
        ("send_sms", ("+15551234567", "test")),
        ("set_flashlight", (True,)),
    ],
)
def test_sensitive_actions_are_denied_by_default(method, args):
    with pytest.raises(CapabilityDenied):
        getattr(PhoneActions(), method)(*args)


def test_explicit_policy_does_not_silently_add_an_integration():
    actions = PhoneActions(
        CapabilityPolicy(sms_enabled=True, flashlight_enabled=True)
    )

    with pytest.raises(NotImplementedError):
        actions.send_sms("+15551234567", "test")
    with pytest.raises(NotImplementedError):
        actions.set_flashlight(True)
