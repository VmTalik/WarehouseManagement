from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order_item import OrderItem


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    quantity: Mapped[int]
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")
