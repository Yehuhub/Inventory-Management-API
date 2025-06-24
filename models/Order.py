from sqlalchemy import String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped,mapped_column, relationship, validates
from datetime import datetime
from data.ORMSetup import Base
from typing import Optional, List
import enum

STATUS = ['pending', 'delivered']


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default='pending')
    delivery_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    client: Mapped["Client"] = relationship(back_populates="orders")
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


    @validates("status")
    def validate_status(self, key, value: str) -> str:
        if value not in STATUS:
            raise ValueError(f"Invalid status '{value}'. Must be one of {STATUS}.")
        return value

    @validates("delivery_date")
    def validate_delivery_date(self, key, value: datetime.date) -> datetime.date:
        if value is None:
            raise ValueError("Delivery date cannot be null.")
        return value
    
    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "user_id": self.user_id,
            "status": self.status,
            "delivery_date": self.delivery_date, #might need isoformat
            "created_at": self.createdAt.isoformat(),
            "updated_at": self.updatedAt.isoformat()
        }
