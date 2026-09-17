"""Capability policy for the phone stub.

The default policy is intentionally restrictive. Hardware and provider
integrations must be supplied explicitly by a later change.
"""

from dataclasses import dataclass


class CapabilityDenied(PermissionError):
    """Raised before a disabled capability can perform any side effect."""


@dataclass(frozen=True)
class CapabilityPolicy:
    """Explicit capability switches; both sensitive capabilities default off."""

    sms_enabled: bool = False
    flashlight_enabled: bool = False

    def snapshot(self) -> dict[str, bool]:
        """Return the public, JSON-compatible capability state."""

        return {
            "sms": self.sms_enabled,
            "flashlight": self.flashlight_enabled,
        }

    def require(self, capability: str) -> None:
        """Allow a capability only when its explicit switch is enabled."""

        enabled = {
            "sms": self.sms_enabled,
            "flashlight": self.flashlight_enabled,
        }.get(capability)
        if enabled is None:
            raise CapabilityDenied(f"unknown capability: {capability}")
        if not enabled:
            raise CapabilityDenied(f"capability disabled by policy: {capability}")


DEFAULT_POLICY = CapabilityPolicy()


class PhoneActions:
    """Future action boundary; no provider or device integration is included."""

    def __init__(self, policy: CapabilityPolicy = DEFAULT_POLICY) -> None:
        self.policy = policy

    def send_sms(self, recipient: str, message: str) -> None:
        """Guard SMS before a future provider could be called."""

        del recipient, message
        self.policy.require("sms")
        raise NotImplementedError("SMS integration is not part of this stub")

    def set_flashlight(self, enabled: bool) -> None:
        """Guard flashlight access before a future device driver is called."""

        del enabled
        self.policy.require("flashlight")
        raise NotImplementedError("flashlight integration is not part of this stub")
