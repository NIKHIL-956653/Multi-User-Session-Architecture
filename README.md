# Multi-User Session Architecture
### AI Chat System with Per-User Context Management

An AI-powered multi-user chat system where each user gets their own 
private session with persistent chat history stored in MongoDB.

## What It Does
User logs in with username
↓
Unique Session ID created (UUID)
↓
User chats with Gemini AI
↓
Full conversation saved to MongoDB
↓
User logs out and comes back later
↓
Previous chat history loaded automatically!

## Tech Stack

- **Python** — core language
- **MongoDB** — stores per-user chat history permanently
- **FastAPI** — REST API backend with Swagger docs
- **Streamlit** — multi-user chat UI
- **OpenRouter (Gemini 2.0 Flash)** — LLM for responses
- **Ollama (Qwen)** — local LLM fallback
- **python-dotenv** — environment management

## Project Structure
Multi-User-Session-Architecture/
├── app/
│   ├── session_manager.py  # MongoDB session CRUD operations
│   ├── llm_engine.py       # LLM with chat history context
│   ├── streamlit_app.py    # Multi-user chat UI
│   └── fastapi_app.py      # REST API endpoints
├── requirements.txt
├── .gitignore
└── .env                    # API keys (not committed)

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/NIKHIL-956653/Multi-User-Session-Architecture.git
cd Multi-User-Session-Architecture
```

### 2. Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
OPENROUTER_API_KEY=your_openrouter_key
MONGODB_URI=mongodb://localhost:27017

### 5. Start MongoDB
Make sure MongoDB is running locally!

## Run

### Streamlit UI (Multi-user chat)
```bash
streamlit run app/streamlit_app.py
```

### FastAPI Backend
```bash
python -m uvicorn app.fastapi_app:app --reload
```

Then open: `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /session/create | Create or get existing session |
| POST | /chat | Send message, get AI response |
| GET | /history/{session_id} | Get full chat history |

## How It Works

### Session Management
Each user gets a unique UUID session ID stored in MongoDB.
Returning users load their existing session automatically.

### Chat with Memory
User asks Q1 → saved to MongoDB
User asks Q2 → Q1 fetched from MongoDB
→ Q1 + Q2 sent to Gemini
→ Gemini answers with full context!

### Multi-User Isolation
Nikhil session   → his history only
Sai Kumar session → his history only
They NEVER mix! ✅

## Results

- ✅ Multiple users chatting simultaneously
- ✅ Per-user chat history stored in MongoDB
- ✅ LLM remembers full conversation context
- ✅ REST API with Swagger documentation
- ✅ Streamlit UI with login/logout

## Author

**Nikhil Chandra Sairam Tokala**
AI/ML Engineer | GenAI Engineer | DevOps
Dubai, UAE
[LinkedIn](https://linkedin.com/in/nikhil-chandra-133ncsr200233) |
[GitHub](https://github.com/NIKHIL-956653)
