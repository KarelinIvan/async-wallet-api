from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.wallet import Wallet


class WalletRepository:
    """Класс для работы с базой данных."""

    def __init__(self, session: AsyncSession):
        """Сохраняет сессию."""
        self.session = session

    async def get_by_id(self, wallet_id: UUID) -> Wallet | None:
        """
        Метод получает ID кошелька.

        Args:
            wallet_id (UUID): Уникальный идентификатор кошелька.

        Returns:
            Wallet | None: Возвращает кошелек или None, если кошелёк не найден.
        """
        query = select(Wallet).where(Wallet.id == wallet_id)
        result = await self.session.exec(query)
        return result.first()
