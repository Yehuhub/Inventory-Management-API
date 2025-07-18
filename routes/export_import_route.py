from flask import Blueprint, jsonify
from utils.export_excel import export_table_to_excel
from utils.csv_importer import import_items_categories_from_csv
from http import HTTPStatus

export_import_router = Blueprint("export", __name__)

# route to export a selected table to excel file
@export_import_router.get("/export/<table_name>")
def export_table(table_name):
    try:
        message = export_table_to_excel(table_name)
        return jsonify({"message": message})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
# route to import a csv
@export_import_router.post("/import/csv")
def import_items_and_categories_csv_route():
    import_items_categories_from_csv()
    return jsonify("Items and Categories imported"), HTTPStatus.OK
