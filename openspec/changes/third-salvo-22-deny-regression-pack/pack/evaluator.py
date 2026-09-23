"""Pure offline evaluator for the T3-22 eligibility contract."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

SLOT = "T3-22"
INCLUDED = "INCLUDED"
ON_DEMAND = "ON_DEMAND"
ULTRA = "Ultra"


def evaluate(request: Any) -> dict[str, Any]:
    """Evaluate one request without I/O, lookups, or fallback routing."""

    reason_codes: set[str] = set()
    if not isinstance(request, Mapping):
        reason_codes.add("INVALID_REQUEST")
        return _deny(reason_codes)

    if request.get("slot") != SLOT:
        reason_codes.add("INVALID_REQUEST")

    entitlement = request.get("entitlement")
    if entitlement != INCLUDED:
        reason_codes.add("ENTITLEMENT_NOT_INCLUDED")
        if entitlement == ON_DEMAND:
            reason_codes.add("ON_DEMAND_NOT_ALLOWED")

    if request.get("tier") != ULTRA:
        reason_codes.add("TIER_NOT_ULTRA")

    if reason_codes:
        return _deny(reason_codes)

    return {
        "decision": "ALLOW",
        "slot": SLOT,
        "reason_codes": [],
        "fallback": None,
    }


def _deny(reason_codes: set[str]) -> dict[str, Any]:
    return {
        "decision": "DENY",
        "slot": SLOT,
        "reason_codes": sorted(reason_codes),
        "fallback": None,
    }
