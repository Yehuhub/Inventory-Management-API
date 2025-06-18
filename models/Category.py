from sqlalchemy import String
from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship, mapped_column, Mapped
from typing import List
from models import Item

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    items: Mapped[List['Item']] = relationship("Item", back_populates="category")

    @validates('name')
    def validate_name(self, key, value):
        if not value.isalpha():
            raise ValueError("Category name must only contain letters")
        return value