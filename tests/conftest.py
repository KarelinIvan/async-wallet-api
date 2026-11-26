import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.database.session import get_session
from app.main import app
from app.models.wallet import Wallet


@pytest_asyncio.fixture(scope="session")
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


@pytest_asyncio.fixture(scope="session")
async def concurrent_test_engine():
    """
    Фикстура создаёт движек для тестовой базы данных с поддержкой одновременных
    подключений.
    yield приостанавливает фикстуру до окончания теста.
    NullPool отключает пул соединений, чтобы каждый тест создавал новое соединение.
    После теста dispose() освобождает пул соединений (даже если тест упал).
    """
    url = settings.TEST_DATABASE_URL

    if not url:
        pytest.fail("TEST_DATABASE_URL не задан")

    engine = create_async_engine(url, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def setup_bd(test_engine):
    """
    Фикстура создаёт таблицы в тестовой базе данных create_all.
    yield приостанавливает фикстуру до окончания теста.
    После окончания всех тестов таблицы удаляются drop_all.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
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


@pytest_asyncio.fixture()
async def session_factory(concurrent_test_engine, setup_bd):
    """
    Фикстура создаёт фабрику сессий для тестовой базы данных.
    yield приостанавливает фикстуру до окончания теста.
    """
    maker = async_sessionmaker(
        bind=concurrent_test_engine, class_=AsyncSession, expire_on_commit=False
    )

    yield maker


@pytest_asyncio.fixture
async def clean_db(session_factory):
    """
    Фикстура очищает все таблицы в тестовой базе данных."""
    yield
    async with session_factory() as session:
        await session.execute(delete(Wallet))
        await session.commit()
