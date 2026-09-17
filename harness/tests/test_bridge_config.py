from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from sovereign_harness.bridge_config import (
    PhoneBridgeConfig,
    SftpSyncConfig,
    VultrMcpHostConfig,
)

pytestmark = pytest.mark.smoke


REPO_ROOT = Path(__file__).parents[2]


def _load_json(relative_path: str) -> dict[str, object]:
    path = REPO_ROOT / relative_path
    return json.loads(path.read_text(encoding="utf-8"))


def test_phone_bridge_template_matches_tailnet_health_contract() -> None:
    config = PhoneBridgeConfig.model_validate(
        _load_json("bridges/termux-phone-mcp/phone-bridge.config.example.json")
    )

    assert config.port == 8081
    assert config.health_path == "/health"
    assert config.tailscale_only is True


def test_olette_box_sftp_template_has_expected_accounts() -> None:
    config = SftpSyncConfig.model_validate(
        _load_json("bridges/sftp/olette-box.sync.config.example.json")
    )

    assert str(config.host) == "100.115.0.111"
    assert config.port == 22
    assert {user.username for user in config.users} == {"bunny", "olivia"}
    assert all("REPLACE_WITH_" in user.identity_file for user in config.users)


def test_vultr_template_is_tailnet_only() -> None:
    config = VultrMcpHostConfig.model_validate(
        _load_json("bridges/vultr/mcp-host.config.example.json")
    )

    assert config.mcp_port == 8000
    assert config.tailnet_only is True
    assert config.tailscale_auth_key_env == "TAILSCALE_AUTH_KEY"


def test_sftp_schema_rejects_private_key_bytes() -> None:
    data = _load_json("bridges/sftp/olette-box.sync.config.example.json")
    users = data["users"]
    assert isinstance(users, list)
    users[0]["identity_file"] = "-----BEGIN OPENSSH PRIVATE KEY-----"

    with pytest.raises(ValidationError, match="private key material"):
        SftpSyncConfig.model_validate(data)


def test_deployment_templates_contain_no_private_key_material() -> None:
    ssh_config = (
        REPO_ROOT / "bridges/sftp/olette-box.ssh-config.example"
    ).read_text(encoding="utf-8")
    cloud_init = (
        REPO_ROOT / "bridges/vultr/cloud-init.mcp-host.example.yaml"
    ).read_text(encoding="utf-8")

    assert "BEGIN " not in ssh_config
    assert "BEGIN " not in cloud_init
    assert "<INJECT_AT_DEPLOY_TIME>" in cloud_init
