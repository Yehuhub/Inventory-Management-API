from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, validates

from data.ORMSetup import Base
from datetime import datetime

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = relationship("Order", back_populates="client")

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty.")
        value = value.strip()
        if not all(part.isalpha() for part in value.split()):
            raise ValueError(f"{key} must contain only letters and spaces.")
        return value

    @validates('address')
    def validate_address(self, key, value):
        if not value or not value.strip():
            raise ValueError("Address cannot be empty.")
        return value.strip()

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value or not value.strip():
            raise ValueError("Phone number cannot be empty.")
        value = value.strip()
        if not value.replace('+', '', 1).isdigit() or not (7 <= len(value) <= 15):
            raise ValueError(
                "Phone number must be digits only (optionally starting with '+') and 7–15 characters long.")
        return value

