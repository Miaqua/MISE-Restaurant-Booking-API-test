import re
from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field, field_validator


SLOT_START = 12
SLOT_END = 22


class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120, examples=["Иван Петров"])
    phone: str = Field(examples=["+79991234567"])
    booking_date: date = Field(examples=["2026-09-15"])
    booking_time: time = Field(examples=["19:00"])
    guests: int = Field(ge=1, le=12, examples=[4])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = " ".join(value.strip().split())
        if len(value) < 2 or not re.fullmatch(r"[A-Za-zА-Яа-яЁё]+(?:[ -][A-Za-zА-Яа-яЁё]+)*", value):
            raise ValueError("Имя должно содержать только буквы, пробелы и дефис")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"(?:\+7|8)\d{10}", value):
            raise ValueError("Введите корректный номер: +7 или 8, 10 цифр")
        return value

    @field_validator("booking_time")
    @classmethod
    def validate_time(cls, value: time) -> time:
        if value.second != 0 or value.microsecond != 0 or value.minute != 0 or not SLOT_START <= value.hour <= SLOT_END:
            raise ValueError("Время бронирования должно быть слотом с 12:00 до 22:00 с шагом 1 час")
        return value


class BookingOut(BookingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str = Field(pattern=r"^(active|cancelled)$")
