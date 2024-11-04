import pytest
from fastapi import FastAPI
from core import db_helper
from src.models import Base
from src.main import create_app
from src.core import create_db_helper
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope='function', autouse=True)
async def setup_db():
    test_db_helper = create_db_helper(test_db=True)
    engine = test_db_helper.engine
    # Создание таблиц в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_db_helper
    # Удаление таблиц после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def app(setup_db) -> FastAPI:
    app = create_app()
    app.dependency_overrides[db_helper.session_getter] = setup_db.session_getter
    yield app


@pytest.fixture(scope="function")
async def ac(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
def product_payload():
    return {
        "name": "Эхолот",
        "description": "Точный эхолот",
        "price": 52000,
        "quantity": 10
    }


@pytest.fixture(scope="function")
def order_payload():
    return {
        "order_items": [{"quantity": 3, "product_id": 1}]
    }
