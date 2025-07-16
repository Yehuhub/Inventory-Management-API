from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import DB_IP, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Create an engine (this string should actually be in a .env file)
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}")

# Base class for models
Base = declarative_base()

# Session factory
Session = sessionmaker(bind=engine)

def get_db():
    return Session()

