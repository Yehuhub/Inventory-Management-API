from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from data.ORMSetup import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    item: Mapped["Item"] = relationship(back_populates="order_items")

@validates('quantity')
    def validate_quantity(self, key, value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return value
