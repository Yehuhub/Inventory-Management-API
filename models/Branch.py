from sqlalchemy import ForeignKey
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from typing import List, Optional

class Branch(Base):
    __tablename__ = 'branches'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)

    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)

    # manager has to be optional since branch can be created first, and so it doesnt have a manager at first
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    manager: Mapped[Optional['User']] = relationship('User', back_populates="managed_branches", foreign_keys=[manager_id])

    item_stocks: Mapped[List['ItemStock']] = relationship("ItemStock", back_populates="branch")

    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='branch')

    users: Mapped[List['User']] = relationship("User", back_populates="branch", foreign_keys='User.branch_id')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "manager_id": self.manager_id
        }

    @validates('name')
    def validate_name(self, key, value):
        if not all(part.isalpha() for part in value.split()):
            raise ValueError("Names can only contain letters")
        return value