from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from data.ORMSetup import Base
from datetime import datetime
from typing import List
from models import Order


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    orders: Mapped[List["Order"]] = relationship(back_populates="client")

    @validates('first_name', 'last_name')
    def validate_name(self, key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty.")
        value = value.strip()
        if not all(part.isalpha() for part in value.split()):
            raise ValueError(f"{key} must contain only letters and spaces.")
        return value

    @validates('address')
    def validate_address(self, key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Address cannot be empty.")
        return value.strip()

    @validates('phone_number')
    def validate_phone_number(self, key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Phone number cannot be empty.")
        value = value.strip()
        if not value.replace('+', '', 1).isdigit() or not (7 <= len(value) <= 15):
            raise ValueError("Phone number must be digits only (optionally starting with '+') and 7–15 characters long.")
        return value
