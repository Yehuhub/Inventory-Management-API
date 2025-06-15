from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

# Create an engine (SQLite for this example)
engine = create_engine("postgresql+psycopg2://yehu:Aa123456@localhost:5432/test_db")

# Base class for models
Base = declarative_base()

# Session factory
Session = sessionmaker(bind=engine)
session = Session()