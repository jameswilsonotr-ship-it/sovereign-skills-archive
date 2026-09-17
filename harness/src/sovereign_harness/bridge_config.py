"""Pydantic contracts for the offline bridge deployment templates."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_validator


class PhoneBridgeConfig(BaseModel):
    """Termux phone health listener configuration."""

    model_config = ConfigDict(extra="forbid")

    host: str = "<TAILSCALE_PHONE_IP>"
    port: int = Field(default=8081, ge=1, le=65535)
    health_path: Literal["/health"] = "/health"
    tailscale_only: Literal[True] = True

    @field_validator("host")
    @classmethod
    def host_is_present(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("phone host must not be empty")
        return value


class SftpUserConfig(BaseModel):
    """One key-path-only SFTP identity; private key bytes never belong here."""

    model_config = ConfigDict(extra="forbid")

    username: Literal["bunny", "olivia"]
    identity_file: str = Field(min_length=1)

    @field_validator("identity_file")
    @classmethod
    def identity_file_is_a_path_placeholder(cls, value: str) -> str:
        if "BEGIN " in value or "PRIVATE KEY" in value:
            raise ValueError("identity_file must be a path, not private key material")
        return value


class SftpSyncConfig(BaseModel):
    """Offline-validated SFTP sync target for olette-box."""

    model_config = ConfigDict(extra="forbid")

    host: IPvAnyAddress
    port: int = Field(default=22, ge=1, le=65535)
    users: tuple[SftpUserConfig, ...] = Field(min_length=2)
    remote_root: str = Field(min_length=1)
    known_hosts_file: str = Field(min_length=1)

    @field_validator("users")
    @classmethod
    def expected_users_are_present(
        cls, value: tuple[SftpUserConfig, ...]
    ) -> tuple[SftpUserConfig, ...]:
        usernames = {user.username for user in value}
        if usernames != {"bunny", "olivia"}:
            raise ValueError("SFTP template must contain exactly bunny and olivia")
        return value


class VultrMcpHostConfig(BaseModel):
    """Tailnet-only MCP host settings used by the cloud-init sketch."""

    model_config = ConfigDict(extra="forbid")

    hostname: str = Field(min_length=1)
    tailnet_bind_host: str = Field(min_length=1)
    mcp_port: int = Field(default=8000, ge=1, le=65535)
    tailscale_auth_key_env: str = Field(min_length=1)
    tailnet_only: Literal[True] = True


__all__ = [
    "PhoneBridgeConfig",
    "SftpSyncConfig",
    "SftpUserConfig",
    "VultrMcpHostConfig",
]
