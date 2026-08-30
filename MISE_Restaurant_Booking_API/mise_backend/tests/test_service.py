from datetime import date, timedelta

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models.booking import Base
from app.services.booking_service import BookingService, SlotConflictError


@pytest.mark.asyncio
async def test_service_rejects_occupied_slot():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with factory() as session:
        service = BookingService(session)
        kwargs = dict(name="Иван", phone="89991234567", booking_date=date.today()+timedelta(days=1), booking_time=__import__('datetime').time(19,0), guests=2)
        await service.create(**kwargs)
        with pytest.raises(SlotConflictError):
            await service.create(**kwargs)
    await engine.dispose()
