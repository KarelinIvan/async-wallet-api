class WalletNotFoundError(Exception):
    """Кошелёк не найден."""


class InsufficientFundsError(Exception):
    """На балансе недостаточно средств для списания."""
