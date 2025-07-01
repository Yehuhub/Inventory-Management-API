from flask import Flask, g, jsonify
from models import Branch, Category, Client, Item, ItemStock, Order, OrderItem, Price, Transaction, User
from repository.user_repository import UserRepository
from repository.branch_repository import BranchRepository
from data.ORMSetup import get_db
from data.ORMSetup import engine, Base
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from routes.item_route import item_router
from routes.order_route import order_router
from routes.user_route import user_router
from routes.branch_route import branch_router
from routes.client_route import client_router
from routes.category_route import category_router
from http import HTTPStatus
from utils.csv_importer import import_from_csv

Base.metadata.create_all(engine)


app = Flask(__name__)

# custom error handler for HTTP exceptions
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "error": e.name,               # e.g., "Not Found"
        "message": e.description       # your custom message, if provided
    }).data
    response.content_type = "application/json"
    return response

# custom error handler for SQLAlchemy errors(all db errors will return 500)
@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    return jsonify({
        "error": "Database Error",
        "message": "An unexpected database error occurred"
    }), 500

# db session factory called on each request
@app.before_request
def create_db_session():
    g.db = get_db()  # Create a new session for each request

# db session teardown called after each request
@app.teardown_request
def close_db_session(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close() 

@app.get("/csv")
def import_csv():
    import_from_csv()
    return jsonify("yeah buddy"), HTTPStatus.OK


#==================Setup router blueprints==================#

app.register_blueprint(item_router, url_prefix="/items")
app.register_blueprint(order_router, url_prefix="/orders")
app.register_blueprint(user_router, url_prefix="/users")
app.register_blueprint(branch_router, url_prefix="/branches")
app.register_blueprint(client_router, url_prefix="/clients")
app.register_blueprint(category_router, url_prefix="/categories")



if __name__ == "__main__":
    app.run(debug=True)