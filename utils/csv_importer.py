from flask import g
from models import Item, Category
import csv
from settings import CSV_IMPORT_FILE_PATH
from services.category_service import create_category, get_category_by_name
from services.item_service import create_item
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError

# csv format:
# item_name,item_description,category_name

def import_items_categories_from_csv():
    db = g.db
    category_cache = {}
    with open(CSV_IMPORT_FILE_PATH, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            item_name = row["item_name"].strip()
            item_description = row["item_description"].strip()
            category_name = row["category_name"].strip()

            if not item_name or not category_name:
                continue

            if category_name in category_cache:
                category = category_cache[category_name]
            else:
                try:
                    category = get_category_by_name(db, category_name)
                except BadRequest:
                    new_category = Category(name=category_name)
                    try:
                        category = create_category(db, new_category)
                    except ValueError as ve:
                        print(f"Error Creating category: {ve}")    
                        continue
                    except IntegrityError as e:
                        if 'unique constraint' in str(e.orig).lower() or 'uq_' in str(e.orig).lower():
                            print("Duplicate entry detected.")
                        else:
                            print(f"Integrity error: {e}")
                        continue
                    except Exception as e:
                        print(f"Error Creating item: {e}")    
                        continue
                category_cache[category_name] = category

            new_item = Item(name=item_name, description=item_description, category_id=category.id)
            try:
                create_item(db, new_item)
            except IntegrityError as e:
                if 'unique constraint' in str(e.orig).lower() or 'uq_' in str(e.orig).lower():
                    print("Duplicate entry detected.")
                else:
                    print(f"Integrity error: {e}")
            except Exception as e:
                print(f"Error Creating item: {e}")    