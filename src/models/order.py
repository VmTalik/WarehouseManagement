from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import func
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order_item import OrderItem


class StatusEnum(str, Enum):
    during = "в процессе"
    sent = "отправлен"
    delivered = "доставлен"


class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.during)
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
