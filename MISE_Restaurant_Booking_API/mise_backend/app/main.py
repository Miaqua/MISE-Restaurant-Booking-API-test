from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.bookings import router as bookings_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="MISE Restaurant Booking API",
    description="REST API for restaurant table reservations.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(bookings_router)


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    return {"service": "MISE Restaurant Booking API", "docs": "/docs"}
