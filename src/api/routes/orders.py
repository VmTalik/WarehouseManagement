from fastapi import APIRouter, status, Depends
from schemas import (
    OrderCreate,
    OrderCreateResponse,
    OrderReadResponse,
    OrderUpdate,
    OrderUpdateResponse
)
from crud import OrderCRUDRepository
from api.dependencies import get_repository

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
        order_create: OrderCreate,
        order_repo: OrderCRUDRepository = Depends(get_repository(repo_type=OrderCRUDRepository))
):
    return await order_repo.create_order(order_create=order_create)


@router.get("/", response_model=list[OrderReadResponse], status_code=status.HTTP_200_OK)
async def get_orders_list(
        offset: int = 0,
        limit: int = 20,
        order_repo: OrderCRUDRepository = Depends(get_repository(repo_type=OrderCRUDRepository))
):
    return await order_repo.get_orders_list(offset=offset, limit=limit)


@router.get("/{id}", response_model=OrderReadResponse, status_code=status.HTTP_200_OK)
async def get_order_by_id(
        id: int,
        order_repo: OrderCRUDRepository = Depends(get_repository(repo_type=OrderCRUDRepository))
):
    return await order_repo.get_order_by_id(order_id=id)


@router.patch("/{id}", response_model=OrderUpdateResponse, status_code=status.HTTP_200_OK)
async def update_order_status(
        id: int,
        order_update: OrderUpdate,
        order_repo: OrderCRUDRepository = Depends(get_repository(repo_type=OrderCRUDRepository))

):
    return await order_repo.update_order_status(order_id=id, order_update=order_update)
