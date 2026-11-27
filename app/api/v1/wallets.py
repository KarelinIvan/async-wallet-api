from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_wallet_service
from app.schemas.wallet import OperationRequest, WalletResponse
from app.services.exceptions import InsufficientFundsError, WalletNotFoundError
from app.services.wallet import WalletService

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.get("/{wallet_id}", response_model=WalletResponse)
async def get_wallet(
    wallet_id: UUID,
    service: WalletService = Depends(get_wallet_service),  # noqa: B008
):
    """API: Возвращает кошелёк."""

    try:
        return await service.get_wallet(wallet_id)
    except WalletNotFoundError:
        raise HTTPException(status_code=404, detail="Кошелёк не найден")


@router.post("/{wallet_id}/operation", response_model=WalletResponse)
async def update_wallet(
    wallet_id: UUID,
    data: OperationRequest,
    service: WalletService = Depends(get_wallet_service),  # noqa: B008
):
    """API: Изменяет баланс кошелька."""
    try:
        return await service.process_operation(
            wallet_id, data.operation_type, data.amount
        )
    except WalletNotFoundError:
        raise HTTPException(status_code=404, detail="Кошелёк не найден")
    except InsufficientFundsError:
        raise HTTPException(status_code=400, detail="Недостаточно средств для списания")
