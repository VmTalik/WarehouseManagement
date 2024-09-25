from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, SmallInteger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .order import Order


class OrderItem(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(SmallInteger)
    order: Mapped["Order"] = relationship(back_populates="order_items")
    product: Mapped["Product"] = relationship(back_populates="order_items")
