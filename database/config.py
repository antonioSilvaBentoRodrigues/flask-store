import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Get environment variables
password = f"{os.getenv('DB_PASSWORD')}"
host = f"{os.getenv('HOST')}"
port = f"{os.getenv('PORT')}"
database = f"{os.getenv('DATABASE')}"


# Connect using the environment variables
connection = psycopg2.connect(
        user="postgres",
        password=password,
        host=host,
        port=port,
        database=database
    )
