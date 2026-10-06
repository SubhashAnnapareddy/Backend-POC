from pymongo import MongoClient
from core.config import settings

client = MongoClient(settings.MONGO_URL)
mongo_db = client["student_database"]
student_collection = mongo_db["students"]