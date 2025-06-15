from flask import Flask
from models.User import User
from models.Order import Order
from models.OrderItem import OrderItem
from models.Price import Price
from models.Client import Client

from data.ORMSetup import engine, Base

Base.metadata.create_all(engine)


app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)