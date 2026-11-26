from uuid import uuid4


async def test_get_wallet_not_found(async_client):
    """Тест на получение несуществующего кошелька."""
    wallet_id = uuid4()

    response = await async_client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Кошелёк не найден"
