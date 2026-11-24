from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
)
# Фабрика асинхронных сессий
session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость FastAPI: отдаёт сессию базы данных на время запроса."""
    async with session() as db_session:
        yield db_session
