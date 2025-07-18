from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from data.ORMSetup import Base
from datetime import datetime

class Price(Base):
    __tablename__ = 'prices'

    # item cannot appear twice with same quantity
    __table_args__ = (
        UniqueConstraint('min_quantity', 'item_id', name='uq_item_branch'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    min_quantity: Mapped[int] = mapped_column(nullable=False)
    price_per_unit: Mapped[float] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    item: Mapped["Item"] = relationship(back_populates="prices")

    @validates('min_quantity')
    def validate_min_quantity(self, key, value: int) -> int:
        if value < 0:
            raise ValueError("min_quantity must be a positive integer.")
        return value

    @validates('price_per_unit')
    def validate_price_per_unit(self, key, value: float) -> float:
        if value <= 0:
            raise ValueError("price_per_unit must be a positive number.")
        return float(value)
    
    def to_dict(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "min_quantity": self.min_quantity,
            "price_per_unit": self.price_per_unit,
            "updated_at": self.updated_at.isoformat(),
            "item_name": self.item.name
        }
