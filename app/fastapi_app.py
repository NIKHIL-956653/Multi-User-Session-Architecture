from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.session_manager import create_session, get_chat_history, get_existing_session
from app.llm_engine import chat_with_history

app = FastAPI(title="Multi-User AI Chat API")

class LoginRequest(BaseModel):
    username: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/session/create")
def create_or_get_session(request: LoginRequest):
    existing = get_existing_session(request.username)
    if existing:
        return {"session_id": existing, "status": "existing"}
    session_id = create_session(request.username)
    return {"session_id": session_id, "status": "new"}

@app.post("/chat")
def chat(request: ChatRequest):
    response = chat_with_history(request.session_id, request.message)
    return {"response": response}

@app.get("/history/{session_id}")
def history(session_id: str):
    chat_history = get_chat_history(session_id)
    return {"history": chat_history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)