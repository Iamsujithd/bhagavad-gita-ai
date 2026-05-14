import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import GitaRAG
import json

app = FastAPI(title="Bhagavad Gita AI Chatbot API")

# Setup CORS to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is missing.")
rag = GitaRAG(GROQ_API_KEY)

class ChatRequest(BaseModel):
    query: str
    language: str = "English"
    history: list = []

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        response = rag.get_response(request.query, request.language, request.history)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/daily")
def get_daily_wisdom():
    try:
        data_path = os.path.join(os.path.dirname(__file__), "data", "gita.json")
        with open(data_path, 'r', encoding='utf-8') as f:
            shlokas = json.load(f)
        daily_shloka = random.choice(shlokas)
        return daily_shloka
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
