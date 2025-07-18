from data.ORMSetup import Base
from sqlalchemy.orm import validates, relationship, mapped_column, Mapped
from typing import List
from models import Item

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    items: Mapped[List['Item']] = relationship("Item", back_populates="category")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @validates('name')
    def validate_name(self, key, value):
        if not all(part.isalpha() for part in value.split()):
            raise ValueError("Category name must only contain letters")
        return value