import os
from pymongo import MongoClient


def get_router_info():
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME", "ipa2026_db")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    routers = db["routers"]
    return list(routers.find())
