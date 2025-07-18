import os
from dotenv import load_dotenv


load_dotenv()

CSV_IMPORT_FILE_PATH = os.environ.get("CSV_IMPORT_FILE_PATH")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_IP = os.environ.get("DB_IP")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
