from sqlalchemy import Column, Integer, String, ForeignKey
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship

USER_ROLES = ['admin', 'manager', 'employee']

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) # hashed at the service layer
    role = Column(String, nullable=False)

    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    branch = relationship('Branch', back_populates="users")

    managed_branches = relationship('Branch', back_populates='manager')

    transactions = relationship('Transaction', back_populates='user')
    orders: Mapped[List["Order"]] = relationship(back_populates="user")

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
