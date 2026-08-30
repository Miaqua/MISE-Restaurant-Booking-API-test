from datetime import date, time
from enum import Enum

from sqlalchemy import Date, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BookingStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Base(DeclarativeBase):
    pass


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    booking_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    booking_time: Mapped[time] = mapped_column(Time, nullable=False, index=True)
    guests: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=BookingStatus.ACTIVE.value)
