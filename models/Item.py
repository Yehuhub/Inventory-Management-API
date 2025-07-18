from sqlalchemy import ForeignKey, func, UniqueConstraint, Index
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from typing import List, Optional
from datetime import datetime



class Item(Base):
    __tablename__ = 'items'

    __table_args__ = (
        UniqueConstraint('name', 'category_id', name='uq_name_category'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    category: Mapped['Category'] = relationship("Category", back_populates="items")

    item_stocks: Mapped[List['ItemStock']] = relationship("ItemStock", back_populates="item")

    transactions: Mapped[List['Transaction']] = relationship("Transaction", back_populates="item")

    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="item")
    
    prices: Mapped[List["Price"]] = relationship(back_populates="item")

    
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "category": self.category.name,
            "created_at": self.created_at.isoformat(),
        }

Index(
    'ix_item_name_category_lower',
    func.lower(Item.name),
    Item.category_id,
    unique=True
)