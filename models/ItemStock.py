from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship

# Item_stock -

# ID | branch_id | item_id | quantity | updatedAt


class ItemStock(Base):
    __tablename__ = 'item_stocks'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    branch = relationship("Branch", back_populates="item_stocks")

    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship("Item", back_populates="item_stocks")