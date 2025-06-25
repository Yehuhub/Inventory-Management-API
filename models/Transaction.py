from sqlalchemy import ForeignKey, func
from data.ORMSetup import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from datetime import datetime



TRANSACTION_TYPES = ['send', 'receive']

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    transaction_type: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship("User", back_populates="transactions")

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    item: Mapped['Item'] = relationship("Item", back_populates="transactions")

    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False)
    branch: Mapped['Branch'] = relationship("Branch", back_populates="transactions")

    @validates('transaction_type')
    def validate_transaction_type(self, key, value):
        if value.lower() not in TRANSACTION_TYPES:
            raise ValueError("Transaction type is invalid")
        return value.lower()

    def to_dict(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "descriptin": self.description,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "user_name": self.user.first_name + ' ' + self.user.last_name,
            "item_id": self.item_id,
            "branch_id": self.branch_id,
            "branch_name": self.branch.name
        }