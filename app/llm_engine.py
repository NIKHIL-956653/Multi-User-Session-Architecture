import requests
import os
from dotenv import load_dotenv
from app.session_manager import get_chat_history, add_message

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def chat_with_history(session_id: str, user_message: str) -> str:
    # Get chat history from MongoDB
    history = get_chat_history(session_id)
    
    # Build messages with full history
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Remember the conversation history and answer accordingly."
        }
    ]
    
    # Add previous messages
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["message"]
        })
    
    # Add current message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    # Send to OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-2.0-flash-lite-001",
            "messages": messages
        }
    )
    
    ai_response = response.json()["choices"][0]["message"]["content"]
    
    # Save both messages to MongoDB
    add_message(session_id, "user", user_message)
    add_message(session_id, "assistant", ai_response)
    
    return ai_response


if __name__ == "__main__":
    from app.session_manager import create_session
    
    # Create a test session
    session_id = create_session("Nikhil")
    
    # Chat with history
    print("Q1:")
    r1 = chat_with_history(session_id, "What is JWT authentication?")
    print(f"AI: {r1}\n")
    
    print("Q2:")
    r2 = chat_with_history(session_id, "How do I implement it in FastAPI?")
    print(f"AI: {r2}\n")
    
    print("Q3:")
    r3 = chat_with_history(session_id, "What did I ask you first?")
    print(f"AI: {r3}")