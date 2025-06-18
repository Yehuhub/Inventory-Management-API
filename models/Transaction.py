from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship

# Transactions-

# ID | user_id | item_id | branch_id | type(send/receive/transfer?) | quantity | description | createdAt

TRANSACTION_TYPES = ['send', 'receive']

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    description = Column(String, default="No description")
    created_at = Column(DateTime, default=func.now())


    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="transactions")


    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship("Item", back_populates="transactions")

    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    branch = relationship("Branch", back_populates="transactions")
