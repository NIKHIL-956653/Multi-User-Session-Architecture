import uuid
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

client = MongoClient(MONGODB_URI)
db = client["multi_user_sessions"]
sessions_collection = db["sessions"]

def create_session(username: str) -> str:
    session_id = str(uuid.uuid4())
    session_data = {
        "session_id": session_id,
        "username": username,
        "created_at": datetime.utcnow(),
        "chat_history": []
    }
    sessions_collection.insert_one(session_data)
    print(f"Session created for {username}: {session_id}")
    return session_id

def add_message(session_id: str, role: str, message: str):
    sessions_collection.update_one(
        {"session_id": session_id},
        {"$push": {
            "chat_history": {
                "role": role,
                "message": message,
                "timestamp": datetime.utcnow()
            }
        }}
    )

def get_chat_history(session_id: str) -> list:
    session = sessions_collection.find_one({"session_id": session_id})
    if not session:
        return []
    return session.get("chat_history", [])

def get_existing_session(username: str):
    session = sessions_collection.find_one(
        {"username": username},
        sort=[("created_at", -1)]  # Get most recent session
    )
    if session:
        return session["session_id"]
    return None

def get_all_sessions() -> list:
    sessions = sessions_collection.find({}, {"session_id": 1, "username": 1, "created_at": 1})
    return list(sessions)

if __name__ == "__main__":
    # Test it
    session_id = create_session("Nikhil")
    add_message(session_id, "user", "What is JWT authentication?")
    add_message(session_id, "assistant", "JWT is a JSON Web Token used for secure authentication...")
    
    history = get_chat_history(session_id)
    print("\nChat History:")
    for msg in history:
        print(f"{msg['role']}: {msg['message']}")