from sqlalchemy import Column, Integer, String, ForeignKey
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from typing import List
from models import Branch, Transaction

USER_ROLES = ['admin', 'manager', 'employee']

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False)
    branch: Mapped['Branch'] = relationship('Branch', back_populates="users")

    managed_branches: Mapped[List['Branch']] = relationship('Branch', back_populates='manager')

    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='user')
    
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
