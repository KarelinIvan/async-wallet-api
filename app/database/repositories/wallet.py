from decimal import Decimal
from uuid import UUID

from sqlmodel import col, select, update
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

    async def update_balance(
        self, wallet_id: UUID, amount: Decimal, is_deposit: bool
    ) -> Wallet | None:
        """
        Метод обновляет баланс кошелька.

        Args:
            wallet_id (UUID): Уникальный идентификатор кошелька.
            amount (Decimal): Сумма изменения баланса.
            is_deposit (bool): Флаг операции (True - пополнение, False - списание).

        Returns:
            Wallet | None: Возвращает обновлённый кошелёк или None, если кошелёк
                не найден или баланс для списания недостаточен.
        """

        statement = update(Wallet).where(col(Wallet.id) == wallet_id)

        if not is_deposit:
            statement = statement.where(col(Wallet.balance) >= amount)
            statement = statement.values(
                balance=col(Wallet.balance) - amount
            ).returning(Wallet)
        else:
            statement = statement.values(
                balance=col(Wallet.balance) + amount
            ).returning(Wallet)

        result = await self.session.exec(statement)
        await self.session.commit()
        return result.scalar_one_or_none()
