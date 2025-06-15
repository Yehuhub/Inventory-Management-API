from flask import Flask
from models.User import User
from data.ORMSetup import engine, Base

Base.metadata.create_all(engine)


app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)