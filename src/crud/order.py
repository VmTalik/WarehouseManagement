from .base import BaseCRUDRepository
from models import Order, Product, OrderItem
from schemas import OrderCreate, OrderUpdate
from typing import Sequence
from sqlalchemy import select, Result
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


class OrderCRUDRepository(BaseCRUDRepository):
    async def create_order(self, order_create: OrderCreate) -> Order:
        async with self.async_session.begin():
            order = Order()
            self.async_session.add(order)
            await self.async_session.flush()
            for item in order_create.order_items:
                # Получаем товар с пессиместической блокировкой на обновление
                product_query = await self.async_session.execute(
                    select(Product).where(Product.id == item.product_id).with_for_update()
                )
                product = product_query.scalar_one_or_none()
                if not product:
                    raise HTTPException(status_code=400, detail="Нет такого товара!")
                if product.quantity < item.quantity:
                    raise HTTPException(status_code=400, detail="Недостаточное количество товаров на складе!")
                order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
                self.async_session.add(order_item)
                product.quantity -= item.quantity
        await self.async_session.refresh(order)
        return order

    async def get_orders_list(self, offset: int = 0, limit: int = 20) -> Sequence[Order]:
        stmt = select(Order).options(selectinload(Order.order_items)).offset(offset).limit(limit)
        result: Result = await self.async_session.execute(stmt)
        orders_list = result.scalars().all()
        return orders_list

    async def get_order_by_id(self, order_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id).options(selectinload(Order.order_items))
        result = await self.async_session.execute(stmt)
        order = result.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден!")
        return order

    async def update_order_status(self, order_id: int, order_update: OrderUpdate) -> Order | None:
        order = await self.async_session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Обновление статуса невозможно, заказ не найден!")
        order_update_status = order_update.status
        if order_update_status is not None:
            order.status = order_update_status
        await self.async_session.commit()
        return order
