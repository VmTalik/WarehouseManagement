from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    quantity: int = Field(..., ge=1, description="Количество товаров в заказе")


class OrderItemCreate(OrderItemBase):
    product_id: int


class OrderItemReadForProduct(OrderItemBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    order_id: int
