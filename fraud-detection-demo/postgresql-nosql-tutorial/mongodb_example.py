"""
Minimal MongoDB example: connect using MONGODB_URI, insert a document, find it, print.
Run with: python mongodb_example.py
Requires: MONGODB_URI in environment or defaults to mongodb://localhost:27017
"""
import os
import sys
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(uri, serverSelectionTimeoutMS=5000)

try:
    db = client["tutorial"]
    collection = db["demo"]
    doc = {"name": "example", "value": 1}
    collection.insert_one(doc)
    found = collection.find_one({"name": "example", "value": 1})
    print("Found document:", found)
except (ServerSelectionTimeoutError, ConnectionFailure) as e:
    print("MongoDB connection failed. Is MongoDB running? Set MONGODB_URI if needed.", file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(1)
finally:
    client.close()
