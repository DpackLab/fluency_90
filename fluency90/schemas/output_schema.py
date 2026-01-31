from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field


class OutputCreate(BaseModel):
    output_type: Literal["text", "voice", "structured"]
    payload: Dict[str, Any] = Field(..., min_length=1)


class OutputRead(BaseModel):
    id: int
    output_type: str
    payload: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
