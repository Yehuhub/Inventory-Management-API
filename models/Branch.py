from sqlalchemy import Column, Integer, String, ForeignKey
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship

class Branch(Base):
    __tablename__ = 'branches'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    manager = relationship('User', back_populates="managed_branches")

    phone_number = Column(String, unique=True, nullable=False)

    item_stocks = relationship("ItemStock", back_populates="branch")

    transactions = relationship('Transaction', back_populates='branch')

    users = relationship("User", back_populates="branch")

    @validates('name')
    def validate_name(self, key, value):
        if not value.isalpha():
            raise ValueError("Names can only contain letters")
        return value