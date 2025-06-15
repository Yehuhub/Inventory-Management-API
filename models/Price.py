from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, validates
from data.ORMSetup import Base
from datetime import datetime

class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    #item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    min_quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    #item = relationship("Item", back_populates="prices")

    @validates('min_quantity')
    def validate_min_quantity(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"min_quantity must be a positive integer.")
        return value

    @validates('price_per_unit')
    def validate_price_per_unit(self, key, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("price_per_unit must be a positive number.")
        return float(value)
