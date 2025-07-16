import pandas as pd
from flask import g
from models import User, Branch, Client, Item, ItemStock, Category, Order, OrderItem, Price, Transaction

# Map of supported models to their table names
MODEL_EXPORT_MAP = {
    "users": User,
    "branches": Branch,
    "clients": Client,
    "items": Item,
    "item_stocks": ItemStock,
    "categories": Category,
    "orders": Order,
    "order_items": OrderItem,
    "prices": Price,
    "transactions": Transaction
}

EXPORT_FOLDER = "exported_excels/"


def export_table_to_excel(table_name):

    db = g.db

    if table_name not in MODEL_EXPORT_MAP:
        raise ValueError(f"Table '{table_name}' not supported for export")

    model_class = MODEL_EXPORT_MAP[table_name]
    rows = db.query(model_class).all()

    if not rows:
        return f"No records found in table '{table_name}'"

    try:
        # Convert each model instance to a dictionary
        data = [r.to_dict() for r in rows]

        df = pd.DataFrame(data)
        file_path = f"{EXPORT_FOLDER}{table_name}.xlsx"
        df.to_excel(file_path, index=False)

        return f"Exported {len(data)} records to {file_path}"
    except Exception as e:
        raise RuntimeError(f"Error exporting table '{table_name}': {e}")
