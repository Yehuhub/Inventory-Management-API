import os
from dotenv import load_dotenv


load_dotenv()

CSV_IMPORT_FILE_PATH = os.environ.get("CSV_IMPORT_FILE_PATH")