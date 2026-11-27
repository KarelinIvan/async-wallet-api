import asyncio
from decimal import Decimal


async def test_concurrent_withdraw_drain_to_zero(
    create_wallet, change_balance, get_balance
):
    """
    Тест проверяет, 5 параллельных списания средств по 20 из 100
    (все тесты успешные, итоговый баланс 0).
    """
    # Создаём кошелёк вызывая фикстуру create_wallet
    wallet_id = await create_wallet("100.00")

    # Выполняем списание средств вызывая фикстуру change_balance
    results = await asyncio.gather(
        *(change_balance(wallet_id, "20.00", is_deposit=False) for _ in range(5))
    )
    assert sum(r is not None for r in results) == 5

    assert await get_balance(wallet_id) == Decimal("0.00")


async def test_concurrent_withdraw_no_overdraft(
    create_wallet, change_balance, get_balance
):
    """
    Тест проверяет, 10 параллельных списаний средств по 20 из 100
    (5 успешных, баланс 0, не в минусе)
    """
    wallet_id = await create_wallet("100.00")

    results = await asyncio.gather(
        *(change_balance(wallet_id, "20.00", is_deposit=False) for _ in range(10))
    )

    successful = [r for r in results if r is not None]
    failed = [r for r in results if r is None]

    assert len(successful) == 5
    assert len(failed) == 5
    assert len(results) == 10

    assert await get_balance(wallet_id) == Decimal("0.00")


async def test_concurrent_deposits_no_lost_updates(
    create_wallet, change_balance, get_balance
):
    """Тест проверяет, 20 параллельных пополнений баланса."""
    wallet_id = await create_wallet("50.00")

    results = await asyncio.gather(
        *(change_balance(wallet_id, "10.00", is_deposit=True) for _ in range(20))
    )

    assert all(r is not None for r in results)
    assert await get_balance(wallet_id) == Decimal("250.00")
