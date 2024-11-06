from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

def get_database():
    try:
        client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
        db = client["contact_us_db"]
        return db
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
