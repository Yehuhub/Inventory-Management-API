from sqlalchemy import ForeignKey, DateTime, func, UniqueConstraint
from data.ORMSetup import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
# Item_stock -

# ID | branch_id | item_id | quantity | updatedAt


class ItemStock(Base):
    __tablename__ = 'item_stocks'

    # an item and branch can appear together only once in stock
    __table_args__ = (
        UniqueConstraint('item_id', 'branch_id', name='uq_item_branch_new'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)

    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False)
    branch: Mapped['Branch'] = relationship("Branch", back_populates="item_stocks")

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    item: Mapped['Item'] = relationship("Item", back_populates="item_stocks")

    def to_dict(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "updated_at": self.updated_at.isoformat(),
            "branch_id": self.branch_id,
            "branch_name": self.branch.name,
        }