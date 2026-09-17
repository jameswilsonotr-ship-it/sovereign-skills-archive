"""Offline safety primitives for SMS integrations.

This package intentionally contains no provider client and performs no network
I/O. It is a contract stub for callers that need to exercise SMS safety
behavior before a real transport is introduced.
"""

from .stubs import (
    REDACTED,
    REDACTED_BODY,
    REDACTED_PHONE,
    SmsPolicy,
    SmsSendResult,
    SmsSenderStub,
    redact_mapping,
    redact_phone,
    redact_request,
)

__all__ = [
    "REDACTED",
    "REDACTED_BODY",
    "REDACTED_PHONE",
    "SmsPolicy",
    "SmsSendResult",
    "SmsSenderStub",
    "redact_mapping",
    "redact_phone",
    "redact_request",
]
