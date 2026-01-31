from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from fluency90.models.base import Base


class UserStreak(Base):
    __tablename__ = "user_streaks"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    current_streak: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    last_active_date: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
