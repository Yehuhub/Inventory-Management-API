from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from data.ORMSetup import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)


    order: Mapped["Order"] = relationship(back_populates="items")
    item: Mapped["Item"] = relationship(back_populates="order_items")

    @validates('quantity')
    def validate_quantity(self, key, value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return value

    def to_dict(self):
        return{
            "order_id": self.order_id,
            "item_id": self.item_id,
            "item_name": self.item.name,
            "quantity": self.quantity,
            "price": self.price
        }