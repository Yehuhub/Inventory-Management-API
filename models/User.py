from sqlalchemy import ForeignKey
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from typing import List, Optional

USER_ROLES = ['manager', 'employee']

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    branch_id: Mapped[Optional[int]] = mapped_column(ForeignKey('branches.id'), nullable=True)
    branch: Mapped['Branch'] = relationship('Branch', back_populates="users", foreign_keys=[branch_id])

    managed_branches: Mapped[List['Branch']] = relationship('Branch', back_populates='manager', foreign_keys='Branch.manager_id')

    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='user')

    orders: Mapped[List['Order']] = relationship("Order", back_populates='user')

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "role": self.role,
            "branch_id": self.branch_id
        }

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value.isalpha():
            raise ValueError("Names can only contain letters")
        return value
    
    @validates('role')
    def validate_role(self, key, value):
        if value not in USER_ROLES:
            raise ValueError("Invalid user role")
        return value
    
    @validates('branch_id')
    def validate_employee_branch(self, key, value):
        print(f"role: {self.role}, value: {value}")
        if self.role == 'employee' and value is None:
            print("in if!")
            raise ValueError("Employees must have a branch")
        return value
