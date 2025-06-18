from sqlalchemy import ForeignKey, DateTime, func
from data.ORMSetup import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from models import User, Item, Branch

# Transactions-

# ID | user_id | item_id | branch_id | type(send/receive/transfer?) | quantity | description | createdAt

TRANSACTION_TYPES = ['send', 'receive']

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship("User", back_populates="transactions")

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    item: Mapped['Item'] = relationship("Item", back_populates="transactions")

    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False)
    branch: Mapped['Branch'] = relationship("Branch", back_populates="transactions")
