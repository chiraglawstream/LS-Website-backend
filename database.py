from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_database():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
        db = client["contact_us_db"]
        return db["contacts"]  # Return the specific collection
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
