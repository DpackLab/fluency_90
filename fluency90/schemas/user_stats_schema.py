from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserMeStats(BaseModel):
    current_streak: int
    active_today: bool
    session_active: bool
    session_started_at: Optional[datetime] = None
    has_output_today: bool
    blocked_without_output: bool
