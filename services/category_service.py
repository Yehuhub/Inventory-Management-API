from repository.category_repository import CategoryRepository
from werkzeug.exceptions import NotFound, BadRequest
from models import Category

def get_category_by_id(db, category_id):
    category_repository = CategoryRepository(db)
    category = category_repository.get_by_id(category_id)
    if not category:
        raise NotFound("Category not found")
    return category

def get_all_categories(db):
    category_repository = CategoryRepository(db)
    categories = category_repository.list_all()
    if not categories:
        raise NotFound("No categories found")
    return categories

def create_category(db, new_category):
    category_repository = CategoryRepository(db)
    if(category_repository.is_category_exists_case_insensitive(new_category.name)):
        raise ValueError("Category already exists")
    return category_repository.create(new_category)

def delete_category(db, category_id):
    category_repository = CategoryRepository(db)
    category = category_repository.get_by_id(category_id)
    if not category:
        raise NotFound("Category not found")
    category_repository.delete(category)

def update_category(db, category_id, updates):
    category_repository = CategoryRepository(db)
    category = category_repository.get_by_id(category_id)
    if not category:
        raise NotFound("Category not found")
    if not updates:
        raise BadRequest("No updates provided")
    return category_repository.update(category, updates)

def get_items_by_category_id(db, category_id):
    category_repository = CategoryRepository(db)
    category = category_repository.get_by_id(category_id)
    if not category:
        raise NotFound("Category not found")
    if not category.items:
        raise NotFound("No items found for this category")
    return category.items

def get_items_by_category_name(db, category_name):
    category_repository = CategoryRepository(db)
    items = category_repository.get_items_by_category_name(category_name)
    if not items:
        raise NotFound(f"No items found for category: {category_name}")
    return items

def get_category_by_name(db, category_name):
    category_repository = CategoryRepository(db)
    category = category_repository.get_category_by_name(category_name)
    if not category:
        raise NotFound(f"Category not found: {category_name}")
    return category

def does_category_exists_by_name(db, category_name):
    repo = CategoryRepository(db)
    return repo.is_category_exists_case_insensitive(category_name)