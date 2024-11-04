import asyncio
from httpx import AsyncClient
from .messages import (
    FAILED_CREATE_ORDER,
    FAILED_GET_ORDER,
    FAILED_GET_ORDERS,
    FAILED_UPDATE_ORDER,
    FAILED_CREATE_PRODUCT,
    FAILED_GET_PRODUCT
)


async def create_order(ac: AsyncClient, order_data: dict):
    return await ac.post("/orders/", json=order_data)


async def test_create_get_orders(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    product_id = response.json()["id"]
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    # create orders
    orders_data = [
        {"order_items": [{"quantity": 2, "product_id": product_id}]},
        {"order_items": [{"quantity": 3, "product_id": product_id}]},
        {"order_items": [{"quantity": 5, "product_id": product_id}]}
    ]
    tasks = [create_order(ac, order_data) for order_data in orders_data]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        assert response.status_code == 201, FAILED_CREATE_ORDER
    response = await ac.get(f"/products/{product_id}")
    assert response.status_code == 200, FAILED_GET_PRODUCT
    assert response.json()["quantity"] == 0, "Неправильное оставшееся кол-во товара"  # 10-(2+3+5)=0
    # get orders
    response = await ac.get("/orders/?offset=0&limit=20")
    assert response.status_code == 200, FAILED_GET_ORDERS + "offset=0&limit=20"
    assert len(response.json()) == len(orders_data)
    response = await ac.get("/orders/?offset=0&limit=2")
    assert response.status_code == 200, FAILED_GET_ORDERS + "offset=0&limit=2"
    assert len(response.json()) == 2
    response = await ac.get("/orders/?offset=1&limit=20")
    assert response.status_code == 200, FAILED_GET_ORDERS + "offset=1&limit=20"
    assert len(response.json()) == len(orders_data) - 1


async def test_create_get_order_by_id(ac: AsyncClient, product_payload: dict, order_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    order_payload["order_items"][0]["product_id"] = product_id
    response = await ac.post("/orders/", json=order_payload)
    assert response.status_code == 201, FAILED_CREATE_ORDER
    order_id = response.json()["id"]
    response = await ac.get(f"/orders/{order_id}")
    assert response.status_code == 200, FAILED_GET_ORDER
    order_payload["id"] = response.json()["id"]
    order_payload["created_at"] = response.json()["created_at"]
    order_payload["status"] = response.json()["status"]
    assert order_payload == response.json()


async def test_create_update_order_status(ac: AsyncClient, product_payload: dict, order_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    order_payload["order_items"][0]["product_id"] = product_id
    response = await ac.post("/orders/", json=order_payload)
    assert response.status_code == 201, FAILED_CREATE_ORDER
    order_id = response.json()["id"]
    response = await ac.get(f"/orders/{order_id}")
    assert response.status_code == 200, FAILED_GET_ORDER
    assert response.json()["status"] == "в процессе"
    order_status_update = {"status": "доставлен"}
    response = await ac.patch(f"/orders/{order_id}", json=order_status_update)
    assert response.status_code == 200, FAILED_UPDATE_ORDER
    assert response.json()["status"] == order_status_update["status"], "Статус обновился некорректно"


async def test_create_order_wrong_data(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]

    wrong_order_data = {"order_items": [{"quantity": -3, "product_id": product_id}]}
    response = await ac.post("/orders/", json=wrong_order_data)
    assert response.status_code == 422

    wrong_order_data = {"order_items": [{"product_id": product_id}]}
    response = await ac.post("/orders/", json=wrong_order_data)
    assert response.status_code == 422

    wrong_order_data = {"order_items": [{"quantity": 3, "product_id": 0}]}
    response = await ac.post("/orders/", json=wrong_order_data)
    assert response.status_code == 400


async def test_create_get_by_id_order_wrong_data(ac: AsyncClient, product_payload: dict, order_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    order_payload["order_items"][0]["product_id"] = product_id
    response = await ac.post("/orders/", json=order_payload)
    assert response.status_code == 201, FAILED_CREATE_ORDER
    order_id = response.json()["id"]
    wrong_order_id = 100
    assert wrong_order_id != order_id
    response = await ac.get(f"/orders/{wrong_order_id}")
    assert response.status_code == 404


async def test_create_update_order_status_wrong_data(ac: AsyncClient, product_payload: dict, order_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    order_payload["order_items"][0]["product_id"] = product_id
    response = await ac.post("/orders/", json=order_payload)
    assert response.status_code == 201, FAILED_CREATE_ORDER
    order_id = response.json()["id"]
    order_payload["status"] = response.json()["status"]
    wrong_order_update_data = {"status": "aaa"}
    response = await ac.patch(f"/orders/{order_id}", json=wrong_order_update_data)
    assert response.status_code == 422
