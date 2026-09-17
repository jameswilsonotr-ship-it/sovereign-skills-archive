import socket
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.audit_log import AuditLogger
from scripts.flashlight import OfflineNetworkError, network_guard


def test_network_guard_denies_connections_and_restores_socket():
    original_connect = socket.socket.connect

    with AuditLogger() as audit:
        with network_guard(audit):
            with pytest.raises(OfflineNetworkError):
                socket.create_connection(("example.invalid", 443))

    assert socket.socket.connect is original_connect


def test_flashlight_cli_runs_offline_and_writes_audit(tmp_path):
    test_file = tmp_path / "test_local.py"
    test_file.write_text("def test_local():\n    assert 2 + 2 == 4\n", encoding="utf-8")
    audit_file = tmp_path / "audit.jsonl"
    script = Path(__file__).parents[1] / "scripts" / "flashlight.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            str(test_file),
            "--audit-log",
            str(audit_file),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    assert '"policy": "default_deny"' in audit_text
    assert '"event": "flashlight.complete"' in audit_text
