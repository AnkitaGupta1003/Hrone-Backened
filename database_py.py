# database.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
client = None
db = None
def init_db():
    """Initialize database connection"""
    global client, db
    MONGODB_URL = os.getenv("MONGODB_URL")
    if not MONGODB_URL:
        raise ValueError("MONGODB_URL not found in .env file")
    
    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=3000)  # 3s timeout
        client.server_info()  # Trigger actual connection to catch errors early
        db = client.ecommerce

        # Create indexes
        db.products.create_index("name")
        db.orders.create_index("user_id")
        db.orders.create_index("createdOn")
        print(" MongoDB connected successfully")
    except Exception as e:
        print(" MongoDB connection failed:", e)
        raise


def get_database():
    """Get database instance"""
    if db is None:
        init_db()
    return db

def close_db():
    """Close database connection"""
    global client
    if client:
        client.close()

# Collections
def get_products_collection():
    return get_database().products

def get_orders_collection():
    return get_database().orders

def get_client():
    global client
    print(client)
    if client is None:
        init_db()
    return client