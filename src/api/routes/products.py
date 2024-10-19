from fastapi import APIRouter, status, Depends
from schemas import (
    ProductCreate,
    ProductCreateResponse,
    ProductReadResponse,
    ProductUpdate,
    ProductUpdateResponse
)
from crud import ProductCRUDRepository
from api.dependencies import get_repository

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_create: ProductCreate,
        product_repo: ProductCRUDRepository = Depends(get_repository(repo_type=ProductCRUDRepository))
):
    return await product_repo.create_product(product_create=product_create)


@router.get("/", response_model=list[ProductReadResponse], status_code=status.HTTP_200_OK)
async def get_products_list(
        offset: int = 0,
        limit: int = 10,
        product_repo: ProductCRUDRepository = Depends(get_repository(repo_type=ProductCRUDRepository))
):
    return await product_repo.get_products_list(offset=offset, limit=limit)


@router.get("/{id}", response_model=ProductReadResponse, status_code=status.HTTP_200_OK)
async def get_product_by_id(
        id: int,
        product_repo: ProductCRUDRepository = Depends(get_repository(repo_type=ProductCRUDRepository))
):
    return await product_repo.get_product_by_id(product_id=id)


@router.put("/{id}", response_model=ProductUpdateResponse, status_code=status.HTTP_200_OK)
async def update_product(
        id: int,
        product_update: ProductUpdate,
        product_repo: ProductCRUDRepository = Depends(get_repository(repo_type=ProductCRUDRepository))
):
    return await product_repo.update_product(product_id=id, product_update=product_update)


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        id: int,
        product_repo: ProductCRUDRepository = Depends(get_repository(repo_type=ProductCRUDRepository))
):
    await product_repo.delete_product(product_id=id)
