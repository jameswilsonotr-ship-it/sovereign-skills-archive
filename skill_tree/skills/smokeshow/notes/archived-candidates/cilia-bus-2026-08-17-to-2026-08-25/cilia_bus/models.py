"""Pydantic models for Cilia high-water, receipts, and open legs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Receipt(BaseModel):
    msg_id: str
    action: str
    file_id: Optional[str] = None
    path: Optional[str] = None
    timestamp: datetime = Field(default_factory=utcnow)
    notes: Optional[str] = None


class OpenLeg(BaseModel):
    action: str
    corr: Optional[str] = None
    status: Literal["open", "partial", "acked"] = "open"
    last_seen: datetime = Field(default_factory=utcnow)
    notes: Optional[str] = None


class HighWater(BaseModel):
    """Durable high-water mark that any session can read/write."""

    version: str = "0.1.0"
    updated_at: datetime = Field(default_factory=utcnow)
    last_inbox_msg_id: Optional[str] = None
    last_drive_file_ids: List[str] = Field(default_factory=list)
    receipts: List[Receipt] = Field(default_factory=list)
    open_legs: List[OpenLeg] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)

    def add_receipt(self, receipt: Receipt) -> None:
        self.receipts.append(receipt)
        self.updated_at = utcnow()

    def upsert_leg(self, leg: OpenLeg) -> None:
        for i, existing in enumerate(self.open_legs):
            if existing.action == leg.action:
                self.open_legs[i] = leg
                self.updated_at = utcnow()
                return
        self.open_legs.append(leg)
        self.updated_at = utcnow()
