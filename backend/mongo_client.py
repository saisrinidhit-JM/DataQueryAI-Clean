import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

from datetime import datetime
import re

def parse_dates(data):
    """Recursively convert ISO strings to datetime objects."""
    if isinstance(data, dict):
        return {k: parse_dates(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [parse_dates(v) for v in data]
    elif isinstance(data, str):
        # Match common ISO date formats
        if re.match(r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)?$', data):
            try:
                if 'T' in data:
                    return datetime.fromisoformat(data.replace('Z', '+00:00'))
                else:
                    return datetime.strptime(data, '%Y-%m-%d')
            except:
                return data
    return data

class MongoDBClient:
    def __init__(self):
        # Add a 30s server selection and socket timeout
        self.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=30000, socketTimeoutMS=30000)
        self.db = self.client[DATABASE_NAME]
        print(f"Connected to MongoDB: {DATABASE_NAME}")

    def list_collections(self):
        """Returns a list of all collection names in the database."""
        return self.db.list_collection_names()

    def execute_query(self, query_data):
        """
        Executes a MongoDB query provided in JSON format.
        Expected format: {'collection': 'collection_name', 'action': 'find'|'aggregate', 'filter': {...}, 'pipeline': [...], 'projection': {...}}
        """
        try:
            collection_name = query_data.get('collection')
            action = query_data.get('action')
            
            if not collection_name:
                return {"error": "Missing 'collection' field in the generated query JSON."}
            
            collection = self.db[collection_name]
            result = []

            # Parse dates and handle potential missing keys gracefully
            query_filter = parse_dates(query_data.get('filter', {}))
            query_pipeline = parse_dates(query_data.get('pipeline', []))
            query_projection = query_data.get('projection', None)

            if action == 'find':
                limit = query_data.get('limit', 20)
                # Apply projection if exists
                if query_projection:
                    cursor = collection.find(query_filter, query_projection).limit(limit).max_time_ms(30000)
                else:
                    cursor = collection.find(query_filter).limit(limit).max_time_ms(30000)
                result = list(cursor)
            
            elif action == 'aggregate':
                cursor = collection.aggregate(query_pipeline, maxTimeMS=30000)
                result = list(cursor)
                
            elif action == 'count_documents':
                count = collection.count_documents(query_filter)
                return {"count": count}
            
            else:
                return {"error": f"AI generated an unsupported action: '{action}'. Expected 'find', 'aggregate', or 'count_documents'."}

            # Serialize ObjectId and datetime objects
            return json.loads(json_util.dumps(result))

        except Exception as e:
            return {"error": f"MongoDB execution error: {str(e)}"}

    def get_schema_summary(self):
        """Optional helper to get real schema info if needed, but we rely on docs mostly."""
        summary = {}
        for coll in self.list_collections():
            doc = self.db[coll].find_one()
            if doc:
                summary[coll] = list(doc.keys())
        return summary
