from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Create an engine (this string should actually be in a .env file)
engine = create_engine("postgresql+psycopg2://admin:Aa123456@localhost:5433/dbname")

# Base class for models
Base = declarative_base()

# Session factory
Session = sessionmaker(bind=engine)

def get_db():
    return Session()

