from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class EventPushEnvelope(BaseModel):
    kind: Literal["event"] = "event"
    event: dict[str, Any]
