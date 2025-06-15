from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, validates

from data.ORMSetup import Base
from datetime import datetime
import enum

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    #item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    #item = relationship("Item", back_populates="order_items")

    # Validations
    @validates('quantity')
    def validate_quantity(self, key, value):
        def validate_quantity(self, key, value):
            if not isinstance(value, int) or value <= 0:
                raise ValueError("Quantity must be a positive integer.")
            return value