from flask import Blueprint, jsonify
from utils.export_excel import export_table_to_excel

export_router = Blueprint("export", __name__)


@export_router.get("/export/<table_name>")
def export_table(table_name):
    try:
        message = export_table_to_excel(table_name)
        return jsonify({"message": message})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
