import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.database.session import get_session
from app.main import app


@pytest_asyncio.fixture
async def test_engine():
    """
    Фикстура создаёт движек для тестовой базы данных.
    yield приостанавливает фикстуру до окончания теста.
    После теста dispose() освобождает пул соединений (даже если тест упал).
    """

    url = settings.TEST_DATABASE_URL

    if not url:
        pytest.fail("TEST_DATABASE_URL не задан")

    engine = create_async_engine(url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def setup_bd(test_engine):
    """
    Фикстура создаёт таблицы в тестовой базе данных create_all.
    yield приостанавливает фикстуру до окончания теста.
    После окончания всех тестов таблицы удаляются drop_all.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def test_session(test_engine, setup_bd):
    """
    Фикстура создаёт фабрику сессий для тестовой базы данных.
    yield приостанавливает фикстуру до окончания теста.
    Когда тест закончиться rollback() откатит транзакцию.
    """
    async with test_engine.connect() as connection:
        trans = await connection.begin()

        async with AsyncSession(bind=connection) as session:
            yield session

        await trans.rollback()


@pytest_asyncio.fixture
async def async_client(test_session):
    """
    Фикстура для тестирования API.
    Создаёт AsyncClient с транспортом ASGI и переопределяет зависимость
    get_session, чтобы запросы шли в тестовую БД (test_session).
    """

    async def override_get_session():
        """Функция заглушка, возвращает тестовую сессию."""
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
