from sqlalchemy import Column, Integer, String
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="category")

    @validates('name')
    def validate_name(self, key, value):
        if not value.isalpha():
            raise ValueError("Category name must only contain letters")
        return value