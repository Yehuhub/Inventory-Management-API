from flask import Flask, g, jsonify
from models import Branch, Category, Client, Item, ItemStock, Order, OrderItem, Price, Transaction, User
from repository.user_repository import UserRepository
from repository.branch_repository import BranchRepository
from data.ORMSetup import get_db
from data.ORMSetup import engine, Base
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from routes.item_route import item_router

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

#==================Setup blueprints==================#
app.register_blueprint(item_router, url_prefix="/items")


if __name__ == "__main__":
    app.run(debug=True)