from .base import BaseCRUDRepository
from schemas import ProductCreate, ProductUpdate
from models import Product
from sqlalchemy import select, Result
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


class ProductCRUDRepository(BaseCRUDRepository):
    async def create_product(self, product_create: ProductCreate) -> Product:
        product = Product(**product_create.model_dump())
        self.async_session.add(product)
        await self.async_session.commit()
        await self.async_session.refresh(product)
        return product

    async def get_products_list(self, offset: int = 0, limit: int = 10):
        stmt = select(Product).options(selectinload(Product.order_items)).offset(offset).limit(limit)
        result: Result = await self.async_session.execute(stmt)
        products_list = result.scalars().all()
        return products_list

    async def get_product_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.order_items))
        result = await self.async_session.execute(stmt)
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден!")
        return product

    async def update_product(self, product_id, product_update: ProductUpdate) -> Product | None:
        product = await self.async_session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Обновление невозможно, товар не найден!")
        for name, value in product_update.model_dump().items():
            setattr(product, name, value)
        await self.async_session.commit()
        return product

    async def delete_product(self, product_id) -> None:
        product = await self.async_session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Удаление невозможно, товар не найден!")
        await self.async_session.delete(product)
        await self.async_session.commit()
