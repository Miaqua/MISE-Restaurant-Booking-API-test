from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking_service import BookingNotFoundError, BookingService, SlotConflictError

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(payload: BookingCreate, session: AsyncSession = Depends(get_session)) -> BookingOut:
    try:
        booking = await BookingService(session).create(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except SlotConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return BookingOut.model_validate(booking)


@router.get("", response_model=list[BookingOut])
async def list_bookings(
    date: date | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
) -> list[BookingOut]:
    bookings = await BookingService(session).list(date, skip, limit)
    return [BookingOut.model_validate(item) for item in bookings]


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(booking_id: int, session: AsyncSession = Depends(get_session)) -> BookingOut:
    try:
        booking = await BookingService(session).get(booking_id)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Booking not found") from exc
    return BookingOut.model_validate(booking)


@router.delete("/{booking_id}", response_model=BookingOut)
async def cancel_booking(booking_id: int, session: AsyncSession = Depends(get_session)) -> BookingOut:
    try:
        booking = await BookingService(session).cancel(booking_id)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Booking not found") from exc
    return BookingOut.model_validate(booking)
