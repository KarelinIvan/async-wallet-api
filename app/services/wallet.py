from decimal import Decimal
from uuid import UUID

from app.database.repositories.wallet import WalletRepository
from app.models.wallet import Wallet
from app.schemas.wallet import OperationType
from app.services.exceptions import InsufficientFundsError, WalletNotFoundError


class WalletService:
    """Класс для работы с репозиторием."""

    def __init__(self, repo: WalletRepository):
        """
        Сохраняет данные из репозитория.

        Args:
            repo (WalletRepository) Принимает данные из репозитория.
        """
        self.repo = repo

    async def get_wallet(self, wallet_id: UUID) -> Wallet:
        """
        Метод для получения баланса кошелька.

        Args:
            wallet_id (UUID): Уникальный идентификатор кошелька.

        Returns:
            Wallet: Возвращает баланс кошелька.
        """
        wallet = await self.repo.get_by_id(wallet_id)

        if wallet is None:
            raise WalletNotFoundError("Кошелёк не найден")

        return wallet

    async def process_operation(
        self, wallet_id: UUID, operation_type: OperationType, amount: Decimal
    ) -> Wallet:
        """
        Метод для изменения баланса.

        Args:
            wallet_id (UUID): Уникальный идентификатор кошелька.
            operation_type (OperationType): Тип операции.
            amount (Decimal): Сумма изменения баланса.

        Returns:
            Wallet: Возвращает обновленный баланс кошелька.
        """
        is_deposit = operation_type == OperationType.DEPOSIT

        update_wallet = await self.repo.update_balance(wallet_id, amount, is_deposit)
        if update_wallet is not None:
            return update_wallet
        else:
            wallet = await self.repo.get_by_id(wallet_id)
            if wallet is None:
                raise WalletNotFoundError("Кошелёк не найден")
            else:
                raise InsufficientFundsError("Недостаточно средств для списания")
