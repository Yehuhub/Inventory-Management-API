from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, validates

from data.ORMSetup import Base
from datetime import datetime
import enum

STATUS = ['pending', 'delivered']


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    #client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, nullable=False, default='pending')
    delivery_date = Column(Date, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    # Relationships
    #client = relationship("Client", back_populates="orders")
    user = relationship("User", back_populates="orders")

    # Validations
    @validates('status')
    def validate_status(self, key, value):
        if value not in self.STATUS:
            raise ValueError(f"Invalid status '{value}'. Must be one of {self.STATUS}.")
        return value

    @validates('delivery_date')
    def validate_delivery_date(self, key, value):
        if value is None:
            raise ValueError("Delivery date cannot be null.")
        return value