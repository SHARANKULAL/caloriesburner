# test_mongo.py
from pymongo import MongoClient
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['calorie_db']
    collection = db['users']
    # Insert test document
    test_doc = {"user_id": "test_mongo", "calories": 100, "timestamp": "2025-04-12"}
    collection.insert_one(test_doc)
    print("Inserted test document")
    # Check if it exists
    doc = collection.find_one({"user_id": "test_mongo"})
    print("Found:", doc)
    # Check database
    print("Databases:", client.list_database_names())
except Exception as e:
    print("Error:", str(e))