from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

def get_database():
    try:
        client = MongoClient("mongodb+srv://chiragyadav:9NioCDpLD9OgVt9m@cluster0.fptls.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tls=True, tlsAllowInvalidCertificates=True)
        db = client["contact_us_db"]
        return db["contacts"] 
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
