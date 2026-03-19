import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'bi_dw')
DB_USER = os.getenv('DB_USER', 'bi_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'bi_pass')
