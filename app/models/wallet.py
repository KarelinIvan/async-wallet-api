from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class Wallet(SQLModel, table=True):
    """
    ORM-модель таблицы Wallet.

    id (UUID): Уникальный идентификатор кошелька.
    balance (Decimal): Баланс счёта.
    created_at (datetime): Дата создания кошелька.
    updated_at (datetime): Дата последнего изменения.
    """

    __tablename__ = "wallets"  # type: ignore

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    balance: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
        description="Дата создания кошелька",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs={"onupdate": func.now()},
        description="Дата последнего изменения",
    )
