"""Default-deny and offline-only pytest contracts for the flashlight stub."""

import builtins
import pathlib
import socket
import subprocess

import pytest

from harness.tests.stubs import OfflineFlashlightStub, RecordingAuditSink


@pytest.fixture
def audit_sink():
    return RecordingAuditSink()


@pytest.fixture
def flashlight(audit_sink):
    return OfflineFlashlightStub(audit_sink=audit_sink)


def test_default_policy_denies_every_supported_action(flashlight, audit_sink):
    for action in ("on", "off", "status"):
        decision = flashlight.request(action)

        assert decision == {
            "allowed": False,
            "performed": False,
            "reason": "capability_not_granted",
        }

    assert [event["outcome"] for event in audit_sink.events] == [
        "denied",
        "denied",
        "denied",
    ]


@pytest.mark.parametrize("action", ("", "blink", None, 7, ["on"]))
def test_unknown_or_malformed_actions_are_denied(flashlight, action):
    decision = flashlight.request(action)

    assert decision["allowed"] is False
    assert decision["performed"] is False
    assert decision["reason"] == "unsupported_action"


def test_explicit_capability_only_authorizes_a_simulation(audit_sink):
    flashlight = OfflineFlashlightStub(
        allowed_actions={"status"},
        audit_sink=audit_sink,
    )

    decision = flashlight.request("status")

    assert decision == {
        "allowed": True,
        "performed": False,
        "reason": "explicit_capability",
    }
    assert audit_sink.events[-1] == {
        "event": "flashlight.authorization",
        "action": "status",
        "outcome": "allowed",
        "reason": "explicit_capability",
    }


def test_invalid_intensity_is_denied_before_authorization(audit_sink):
    flashlight = OfflineFlashlightStub(
        allowed_actions={"on"},
        audit_sink=audit_sink,
    )

    decision = flashlight.request("on", intensity="bright")

    assert decision["allowed"] is False
    assert decision["performed"] is False
    assert decision["reason"] == "invalid_intensity"
    assert audit_sink.events[-1]["outcome"] == "denied"


def test_stub_does_not_use_device_or_process_io(
    monkeypatch,
    flashlight,
):
    def forbidden(*args, **kwargs):
        raise AssertionError("device/process I/O is forbidden in this harness")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "open", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)

    decision = flashlight.request("status")

    assert decision["allowed"] is False
    assert decision["performed"] is False
