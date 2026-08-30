from datetime import date, timedelta

import pytest


@pytest.mark.asyncio
async def test_create_booking_returns_201_and_active(client):
    response = await client.post("/bookings", json={
        "name": "Иван Петров",
        "phone": "+79991234567",
        "booking_date": str(date.today()),
        "booking_time": "19:00",
        "guests": 4,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "active"


@pytest.mark.asyncio
async def test_invalid_phone_is_422(client):
    response = await client.post("/bookings", json={
        "name": "Иван",
        "phone": "123",
        "booking_date": str(date.today()),
        "booking_time": "19:00",
        "guests": 2,
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_date_range_is_422(client):
    response = await client.post("/bookings", json={
        "name": "Иван",
        "phone": "89991234567",
        "booking_date": str(date.today() + timedelta(days=91)),
        "booking_time": "19:00",
        "guests": 2,
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_occupied_slot_is_409(client):
    payload = {
        "name": "Иван",
        "phone": "89991234567",
        "booking_date": str(date.today() + timedelta(days=1)),
        "booking_time": "20:00",
        "guests": 2,
    }
    assert (await client.post("/bookings", json=payload)).status_code == 201
    payload["name"] = "Петр"
    assert (await client.post("/bookings", json=payload)).status_code == 409


@pytest.mark.asyncio
async def test_get_and_filter_bookings(client):
    target = date.today() + timedelta(days=2)
    payload = {
        "name": "Анна",
        "phone": "+79991234567",
        "booking_date": str(target),
        "booking_time": "18:00",
        "guests": 3,
    }
    await client.post("/bookings", json=payload)
    response = await client.get("/bookings", params={"date": str(target)})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["booking_date"] == str(target)


@pytest.mark.asyncio
async def test_get_missing_booking_is_404(client):
    response = await client.get("/bookings/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}


@pytest.mark.asyncio
async def test_delete_cancels_without_removing(client):
    payload = {
        "name": "Олег",
        "phone": "89991234567",
        "booking_date": str(date.today()),
        "booking_time": "12:00",
        "guests": 1,
    }
    created = await client.post("/bookings", json=payload)
    booking_id = created.json()["id"]
    cancelled = await client.delete(f"/bookings/{booking_id}")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    fetched = await client.get(f"/bookings/{booking_id}")
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "cancelled"
