from flask import Flask
from models import Branch, Category, Client, Item, ItemStock, Order, OrderItem, Price, Transaction, User

from data.ORMSetup import engine, Base

Base.metadata.create_all(engine)


app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)