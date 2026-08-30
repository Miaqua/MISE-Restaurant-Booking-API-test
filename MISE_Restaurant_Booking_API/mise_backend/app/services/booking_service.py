from datetime import date, datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus


class BookingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, *, name: str, phone: str, booking_date: date, booking_time: time, guests: int) -> Booking:
        today = date.today()
        if booking_date < today:
            raise ValueError("Дата бронирования не может быть раньше сегодняшнего дня")
        if booking_date > today + timedelta(days=90):
            raise ValueError("Дата бронирования не может быть позднее чем через 90 дней")

        stmt = select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.booking_time == booking_time,
            Booking.status == BookingStatus.ACTIVE.value,
        )
        if await self.session.scalar(stmt):
            raise SlotConflictError("Выбранный слот уже занят")

        booking = Booking(
            name=name,
            phone=phone,
            booking_date=booking_date,
            booking_time=booking_time,
            guests=guests,
            status=BookingStatus.ACTIVE.value,
        )
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def list(self, booking_date: date | None = None, skip: int = 0, limit: int = 100) -> list[Booking]:
        stmt = select(Booking).order_by(Booking.booking_date, Booking.booking_time, Booking.id).offset(skip).limit(limit)
        if booking_date:
            stmt = stmt.where(Booking.booking_date == booking_date)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get(self, booking_id: int) -> Booking:
        booking = await self.session.get(Booking, booking_id)
        if booking is None:
            raise BookingNotFoundError("Booking not found")
        return booking

    async def cancel(self, booking_id: int) -> Booking:
        booking = await self.get(booking_id)
        booking.status = BookingStatus.CANCELLED.value
        await self.session.commit()
        await self.session.refresh(booking)
        return booking


class BookingNotFoundError(Exception):
    pass


class SlotConflictError(Exception):
    pass
