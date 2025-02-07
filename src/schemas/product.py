from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, PositiveInt, conint
from schemas.order_item import OrderItemReadForProduct


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80, description="Название")
    description: Optional[str] = Field(default=None, max_length=700, description="Описание")
    price: PositiveInt = Field(..., description="Цена")
    quantity: conint(ge=0) = Field(..., description="Количество на складе")


class ProductCreate(ProductBase):
    pass


class ProductCreateResponse(ProductBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int


class ProductReadResponse(ProductBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    order_items: List[OrderItemReadForProduct]


class ProductUpdate(ProductBase):
    pass


class ProductUpdateResponse(ProductCreateResponse):
    pass


class ProductDelete(ProductBase):
    id: int
