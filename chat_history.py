from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import certifi

from config import MONGODB_URI

mongo_client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=3000  # 🔑 IMPORTANT
)

db = mongo_client["rag_db"]
chat_collection = db["chat_history"]


def store_message(user_id: str, role: str, content: str):
    try:
        chat_collection.insert_one({
            "user_id": user_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })
    except PyMongoError:
        # Fail silently — chat history is optional
        pass


def get_recent_history(user_id: str, limit: int = 6) -> str:
    try:
        messages = chat_collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)

        history = []
        for msg in reversed(list(messages)):
            role = "User" if msg["role"] == "user" else "Assistant"
            history.append(f"{role}: {msg['content']}")

        return "\n".join(history)

    except PyMongoError:
        # If DB is down, return empty history
        return ""
