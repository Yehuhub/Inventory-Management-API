from flask import Flask
from models import Branch, Category, Client, Item, ItemStock, Order, OrderItem, Price, Transaction, User
from repository.user_repository import UserRepository
from repository.branch_repository import BranchRepository
from data.ORMSetup import session

from data.ORMSetup import engine, Base

Base.metadata.create_all(engine)


app = Flask(__name__)

@app.get("/")
def health_check():
    return "test"

if __name__ == "__main__":
    app.run(debug=True)