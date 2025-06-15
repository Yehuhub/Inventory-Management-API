from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship

# Item-

# ID | name | category | description | image | createdAt

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    #image
    
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Category", back_populates="items")

    item_stocks = relationship("ItemStock", back_populates="item")

    transactions = relationship('Transaction', back_populates='item')

    @validates('name')
    def validate_name(self, key, value):
        if not value.isalpha():
            raise ValueError("Names can only contain letters")
        return value
        