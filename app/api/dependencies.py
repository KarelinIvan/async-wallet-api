from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.repositories.wallet import WalletRepository
from app.database.session import get_session
from app.services.wallet import WalletService


async def get_wallet_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> WalletService:
    """Функция, которая создает и возвращает сервис."""
    wallet_repo = WalletRepository(session)
    wallet_service = WalletService(wallet_repo)

    return wallet_service
