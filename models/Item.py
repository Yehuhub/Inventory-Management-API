from sqlalchemy import ForeignKey, DateTime, func
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from typing import List, Optional
from models import Category, ItemStock, Transaction

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(default=func.now())
    
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    category: Mapped['Category'] = relationship("Category", back_populates="items")

    item_stocks = Mapped[List['ItemStock']] = relationship("ItemStock", back_populates="item")

    transactions = Mapped[List['Transaction']] = relationship("Transaction", back_populates="item")

    @validates('name')
    def validate_name(self, key, value):
        if not value.isalpha():
            raise ValueError("Names can only contain letters")
        return value
        