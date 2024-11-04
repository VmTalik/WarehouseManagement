from httpx import AsyncClient
from .messages import (
    FAILED_CREATE_PRODUCT,
    FAILED_GET_PRODUCT,
    FAILED_GET_PRODUCTS,
    FAILED_UPDATE_PRODUCT,
    FAILED_DELETE_PRODUCT,
    FAILED_NUMBER_OF_PRODUCTS
)


async def test_create_get_products(ac: AsyncClient):
    number_of_products = 14
    for i in range(number_of_products):
        product_data = {
            "name": f"Удилище_{i}",
            "description": "Лёгкое удилище",
            "price": 8000,
            "quantity": 10
        }
        response = await ac.post("/products/", json=product_data)
        assert response.status_code == 201, FAILED_CREATE_PRODUCT
    response = await ac.get("/products/?offset=0&limit=10")
    assert response.status_code == 200, FAILED_GET_PRODUCTS + "offset=0&limit=10"
    assert len(response.json()) == 10, FAILED_NUMBER_OF_PRODUCTS + "10"
    response = await ac.get("/products/?offset=0&limit=20")
    assert response.status_code == 200, FAILED_GET_PRODUCTS + "offset=0&limit=20"
    assert len(response.json()) == number_of_products, f"{FAILED_NUMBER_OF_PRODUCTS} {number_of_products}"
    response = await ac.get("/products/?offset=1&limit=14")
    assert response.status_code == 200, FAILED_GET_PRODUCTS + "offset=1&limit=14"
    assert len(response.json()) == number_of_products - 1,  f"{FAILED_NUMBER_OF_PRODUCTS} {number_of_products - 1}"


async def test_create_get_product_by_id(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    response = await ac.get(f"/products/{product_id}")
    assert response.status_code == 200, FAILED_GET_PRODUCT
    product_payload["id"] = response.json()["id"]
    product_payload["order_items"] = []
    assert product_payload == response.json()


async def test_create_update_product(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    product_update_data = {
        "name": "Крючки",
        "description": "",
        "price": 350,
        "quantity": 20
    }
    response = await ac.put(f"/products/{product_id}", json=product_update_data)
    assert response.status_code == 200, FAILED_UPDATE_PRODUCT
    product_update_data["id"] = product_id
    assert response.json() == product_update_data


async def test_delete_product(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    response = await ac.delete(f"/products/{product_id}")
    assert response.status_code == 204, FAILED_DELETE_PRODUCT
    response = await ac.get(f"/products/{product_id}")
    assert response.status_code == 404


async def test_create_product_wrong_data(ac: AsyncClient):
    wrong_product_data = {"name": "Лодка", "description": "Лодка большая", "price": -57000, "quantity": 5}
    response = await ac.post("/products/", json=wrong_product_data)
    assert response.status_code == 422
    wrong_product_data = {"name": "", "description": "Лодка большая", "price": 57000, "quantity": 7}
    response = await ac.post("/products/", json=wrong_product_data)
    assert response.status_code == 422
    wrong_product_data = {"description": "Лодка большая", "price": 57000, "quantity": 5}
    response = await ac.post("/products/", json=wrong_product_data)
    assert response.status_code == 422


async def test_create_get_by_id_product_wrong_data(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    response = await ac.get(f"/products/{-1000}")
    assert response.status_code == 404


async def test_create_update_product_wrong_data(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    product_update_data = {
        "name": "Грузило",
        "description": "",
        "price": -150,
        "quantity": 20
    }
    response = await ac.put(f"/products/{product_id}", json=product_update_data)
    assert response.status_code == 422


async def test_wrong_delete_product(ac: AsyncClient, product_payload: dict):
    response = await ac.post("/products/", json=product_payload)
    assert response.status_code == 201, FAILED_CREATE_PRODUCT
    product_id = response.json()["id"]
    wrong_product_id = 1000
    assert product_id != wrong_product_id
    response = await ac.delete(f"/products/{wrong_product_id}")
    assert response.status_code == 404
