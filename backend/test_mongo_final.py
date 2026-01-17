import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
# DATABASE_NAME = os.getenv("DATABASE_NAME") # "super-j-prod"

dbs_to_test = ["super-j-prod", "superj-prod", "SuperJProd", "test"]
colls_to_test = ["User", "users", "user"]

client = MongoClient(MONGODB_URI)

for db_name in dbs_to_test:
    print(f"\n--- Testing DB: {db_name} ---")
    db = client[db_name]
    for coll_name in colls_to_test:
        try:
            count = db[coll_name].count_documents({})
            print(f"✅ SUCCESS: {db_name}.{coll_name} count = {count}")
        except Exception as e:
            print(f"❌ FAILED: {db_name}.{coll_name} - {str(e)[:100]}...")

# Try to list collections on super-j-prod just to be sure
try:
    print(f"\nListing collections on super-j-prod:")
    print(client["super-j-prod"].list_collection_names())
except Exception as e:
    print(f"❌ FAILED list collections: {e}")
