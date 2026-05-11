from flask import Flask, g, jsonify, request
from models import *
from data.ORMSetup import get_db
from data.ORMSetup import engine, Base
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from routes import *
from utils.auth import decode_token
from http import HTTPStatus
import jwt


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
    }), HTTPStatus.INTERNAL_SERVER_ERROR


# fall back error handler for unexpected errors
# functions that dont have logic to error handling fall here
@app.errorhandler(TypeError)
@app.errorhandler(KeyError)
@app.errorhandler(ValueError)
@app.errorhandler(FileNotFoundError)
def handle_value_error(e):
    return jsonify({
        "error": str(e),
    }), HTTPStatus.BAD_REQUEST

AUTH_EXEMPT_PATHS = {"/api/auth/login"}

# db session factory called on each request
@app.before_request
def create_db_session():
    g.db = get_db()  # Create a new session for each request

@app.before_request
def authenticate_request():
    if request.path in AUTH_EXEMPT_PATHS:
        return

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), HTTPStatus.UNAUTHORIZED

    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        g.user_id = payload["user_id"]
        g.role = payload["role"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), HTTPStatus.UNAUTHORIZED
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

# db session teardown called after each request
@app.teardown_request
def close_db_session(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close() 


#==================Setup router blueprints==================#

app.register_blueprint(auth_router, url_prefix="/api/auth")
app.register_blueprint(item_router, url_prefix="/api/items")
app.register_blueprint(order_router, url_prefix="/api/orders")
app.register_blueprint(user_router, url_prefix="/api/users")
app.register_blueprint(branch_router, url_prefix="/api/branches")
app.register_blueprint(client_router, url_prefix="/api/clients")
app.register_blueprint(category_router, url_prefix="/api/categories")
app.register_blueprint(transaction_router, url_prefix="/api/transactions")
app.register_blueprint(export_import_router, url_prefix="/api/utils")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")