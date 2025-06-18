from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from data.ORMSetup import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models import Branch, Item
# Item_stock -

# ID | branch_id | item_id | quantity | updatedAt


class ItemStock(Base):
    __tablename__ = 'item_stocks'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)

    updated_at: Mapped[DateTime] = mapped_column(default=func.now(), onupdate=func.now())


    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False)
    branch: Mapped['Branch'] = relationship("Branch", back_populates="item_stocks")

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    item = Mapped['Item'] = relationship("Item", back_populates="item_stocks")