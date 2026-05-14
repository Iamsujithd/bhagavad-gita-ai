import os
import random
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="Bhagavad Gita AI Chatbot API")

# Setup CORS to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    language: str = "English"
    history: list = []

class GitaRAG:
    def __init__(self, groq_api_key: str):
        # Initialize Groq LLM
        os.environ["GROQ_API_KEY"] = groq_api_key
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1024,
        )
        
        # Load JSON directly to avoid heavy ML libraries for Vercel
        data_path = os.path.join(os.path.dirname(__file__), "data", "gita.json")
        with open(data_path, 'r', encoding='utf-8') as f:
            self.shlokas = json.load(f)
            
        context_lines = []
        for s in self.shlokas:
            context_lines.append(
                f"Chapter {s['chapter']}, Verse {s['verse']}:\n"
                f"Sanskrit: {s['sanskrit']}\n"
                f"Translation: {s['translation']}"
            )
        self.knowledge_context = "\n\n---\n\n".join(context_lines)
        
        # Setup Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are the Bhagavad Gita AI Chatbot, an intelligent, compassionate, and wise conversational assistant. "
                       "Your purpose is to answer philosophical, ethical, and life-related questions using the timeless wisdom of the Bhagavad Gita. "
                       "Here are the relevant Shlokas (verses) for your knowledge:\n\n{context}\n\n"
                       "Using the provided verses, explain the deeper meaning, provide modern practical guidance, and answer the user's query respectfully. "
                       "Keep your response concise but profound. Do not make up any shlokas; strictly use the context provided. "
                       "IMPORTANT: The user has selected '{language}' as their preferred language. You MUST reply fluently in {language}, ensuring the translation is culturally nuanced and highly accurate. If the language is Kannada, respond fully in Kannada script."),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{question}")
        ])
        
        from operator import itemgetter
        self.chain = (
            {
                "context": itemgetter("context"),
                "question": itemgetter("question"),
                "language": itemgetter("language"),
                "history": itemgetter("history")
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
    def get_response(self, query: str, language: str = "English", history_dicts: list = None):
        if history_dicts is None:
            history_dicts = []
            
        history = []
        for msg in history_dicts[-10:]: # keep last 10 messages for context window
            if msg.get('role') == 'user':
                history.append(HumanMessage(content=msg.get('content', '')))
            elif msg.get('role') == 'ai':
                history.append(AIMessage(content=msg.get('content', '')))
                
        # Generate answer
        answer = self.chain.invoke({
            "context": self.knowledge_context,
            "question": query, 
            "language": language, 
            "history": history
        })
        
        # Determine cited shloka for UI reference box
        cited_shlokas = []
        for s in self.shlokas:
            # If the LLM mentions the chapter/verse or translation snippet
            if f"Chapter {s['chapter']}" in answer or s['translation'][:15] in answer:
                cited_shlokas.append(s)
                break
        
        return {
            "answer": answer,
            "shlokas": cited_shlokas
        }

# Global instance to be initialized lazily
_rag_instance = None

def get_rag():
    global _rag_instance
    if _rag_instance is None:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is missing on Vercel.")
        _rag_instance = GitaRAG(groq_api_key)
    return _rag_instance

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        rag = get_rag()
        response = rag.get_response(request.query, request.language, request.history)
        return response
    except Exception as e:
        print(f"Chat Error: {str(e)}")
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
        print(f"Daily Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)
