from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    """Тип операции."""

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class OperationRequest(BaseModel):
    """Схема входящего запроса."""

    operation_type: OperationType
    amount: Decimal = Field(
        gt=0, max_digits=10, decimal_places=2, description="Сумма операции"
    )


class WalletResponse(BaseModel):
    """Схема ответа API."""

    id: UUID
    balance: Decimal
