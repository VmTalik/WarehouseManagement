from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from models import StatusEnum
from .order_item import OrderItemCreate


class OrderBase(BaseModel):
    created_at: datetime
    status: StatusEnum


class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate]


class OrderCreateResponse(OrderBase):
    id: int
    model_config = ConfigDict(
        from_attributes=True
    )


class OrderReadResponse(OrderCreateResponse):
    order_items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: StatusEnum


class OrderUpdateResponse(OrderCreateResponse):
    pass
