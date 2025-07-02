from repository.base_repository import BaseRepository
from models import Category
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

class CategoryRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Category)

    #gets categories by category name - case insensitive
    def get_category_by_name(self, category_name):
        stmt = select(Category).where(func.lower(Category.name) == category_name.lower()).options(selectinload(Category.items))
        category = self.db.execute(stmt).scalars().first()
        return category if category else None
    
    #gets all items with the same category name - case insensitive
    def get_items_by_category_name(self, category_name):
        category = self.get_category_by_name(category_name)
        return category.items if category else None
    
    #gets all items with the same category id
    def get_items_by_category_id(self, category_id):
        stmt = select(Category).where(Category.id == category_id).options(selectinload(Category.items))
        category = self.db.execute(stmt).scalars().first()
        return category.items if category else None

    def is_category_exists_case_insensitive(self, category_name) -> bool:
        return self.db.query(
            self.db.query(Category).filter(Category.name.ilike(category_name)).exists()).scalar()