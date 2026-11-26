import asyncio
from decimal import Decimal
from uuid import uuid4

from app.models.wallet import Wallet


async def test_get_wallet_not_found(async_client):
    """Тест на получение несуществующего кошелька."""
    wallet_id = uuid4()

    response = await async_client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Кошелёк не найден"


async def test_deposit_balance(async_client, test_session):
    """Тест проверяет увеличение баланса."""
    wallet = Wallet(balance=Decimal("100.00"))
    test_session.add(wallet)
    await test_session.commit()
    await test_session.refresh(wallet)

    response = await async_client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 50},
    )
    assert response.status_code == 200
    assert response.json()["balance"] == "150.00"


async def test_withdraw_insufficient_funds(async_client, test_session):
    """
    Тест проверяет неудачное списание средств,
    когда сумма списания больше чем средства на балансе.
    """
    wallet = Wallet(balance=Decimal("100.00"))
    test_session.add(wallet)
    await test_session.commit()
    await test_session.refresh(wallet)

    response = await async_client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "150.00"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Недостаточно средств для списания"


async def test_withdraw_balance(async_client, test_session):
    """Тест проверяет успешное списание средств."""
    wallet = Wallet(balance=Decimal("100.00"))
    test_session.add(wallet)
    await test_session.commit()
    await test_session.refresh(wallet)

    response = await async_client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "50.00"},
    )
    assert response.status_code == 200


async def test_withdraw_success(async_client, test_session):
    """Тест проверяет успешное списание (баланс сходится в ноль)."""
    wallet = Wallet(balance=Decimal("100.00"))
    test_session.add(wallet)
    await test_session.commit()
    await test_session.refresh(wallet)

    tasks = [
        async_client.post(
            f"/api/v1/wallets/{wallet.id}/operation",
            json={"operation_type": "WITHDRAW", "amount": "20.00"},
        )
        for _ in range(5)
    ]
    response = await asyncio.gather(*tasks)
    assert sum(1 for r in response if r.status_code == 200) == 5
    await test_session.refresh(wallet)
    assert wallet.balance == Decimal("0.00")


async def test_withdraw_unsuccessfully(async_client, test_session):
    """
    Тест проверяет, что при списании превышающем баланс,
    лишние запросы отклоняются.
    """
    wallet = Wallet(balance=Decimal("100.00"))
    test_session.add(wallet)
    await test_session.commit()
    await test_session.refresh(wallet)

    tasks = [
        async_client.post(
            f"/api/v1/wallets/{wallet.id}/operation",
            json={"operation_type": "WITHDRAW", "amount": "20.00"},
        )
        for _ in range(10)
    ]
    response = await asyncio.gather(*tasks)
    assert sum(1 for r in response if r.status_code == 200) == 5
    assert sum(1 for r in response if r.status_code == 400) == 5
    await test_session.refresh(wallet)
    assert wallet.balance == Decimal("0.00")
