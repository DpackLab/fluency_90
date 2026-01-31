from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: Annotated[str, Field(min_length=8)]


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: str
    role: str

    class Config:
        from_attributes = True
