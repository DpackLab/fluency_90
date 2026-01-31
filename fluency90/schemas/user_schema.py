from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

from pydantic import constr

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    role: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDailyStateRead(BaseModel):
    date: date
    active_today: bool
    has_output_today: bool
    blocked_without_output: bool
    current_streak: int
    session_active: bool
    session_started_at: Optional[datetime] = None
