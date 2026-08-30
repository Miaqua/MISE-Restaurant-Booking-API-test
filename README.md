Использовал стек, который и показали, при создании проекта, также использовал нейронку. Делал проект около 3 часов, также потом все проверял

- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 Async
- SQLite + aiosqlite
- Uvicorn
- pytest + pytest-asyncio + httpx
- Alembic
- Docker / Docker Compose

Все эндпоинты:


 POST - `/bookings`  Создать бронь, ответ `201` 
 GET  - `/bookings`  Список броней; фильтр `?date=YYYY-MM-DD`; `skip`/`limit` 
 GET - `/bookings/{id}`  Получить бронь; `404`, если не найдена 
 DELETE - `/bookings/{id}`  Отменить бронь без физического удаления; ответ `200` 

Swagger UI у меня по адресу `/docs`, ReDoc - на `/redoc`.


Локальный запуск

Создать виртуальное окружение

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установить зависимости

```bash
python -m pip install -r requirements.txt
```

Запустить API

```bash
uvicorn app.main:app --reload
```

После запуска:

- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Чтобы тестирование запустить:

Тесты находятся в каталоге `tests/` и используют отдельную SQLite in-memory базу для каждого теста, поэтому тесты не зависят от данных локальной БД.

После установки зависимостей выполните из корня проекта:

```bash
pytest
```

Для подробного вывода:

```bash
pytest -v
```

Для запуска только тестов API:

```bash
pytest tests/test_bookings.py -v
```

Для запуска только тестов сервисного слоя:

```bash
pytest tests/test_service.py -v
```

Для запуска конкретного теста:

```bash
pytest tests/test_bookings.py::test_create_booking_returns_201_and_active -v
```

Тесты проверяют:

- создание брони и статус `active`;
- валидацию некорректного телефона;
- ограничение даты бронирования в 90 дней;
- конфликт при занятом слоте (`409`);
- получение списка и фильтрацию по дате;
- `404` для несуществующей брони;
- отмену брони без физического удаления;
- бизнес-правила сервисного слоя.

