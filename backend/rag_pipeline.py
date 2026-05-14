import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

class GitaRAG:
    def __init__(self, groq_api_key: str):
        # Initialize Groq LLM
        os.environ["GROQ_API_KEY"] = groq_api_key
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1024,
        )
        
        # Load FAISS index
        index_path = os.path.join(os.path.dirname(__file__), "data", "faiss_index")
        print(f"Loading FAISS index from {index_path}...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 2})
        
        # Setup Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are the Bhagavad Gita AI Chatbot, an intelligent, compassionate, and wise conversational assistant. "
                       "Your purpose is to answer philosophical, ethical, and life-related questions using the timeless wisdom of the Bhagavad Gita. "
                       "You have retrieved the following relevant Shlokas (verses) based on the user's question:\n\n{context}\n\n"
                       "Using the provided verses, explain the deeper meaning, provide modern practical guidance, and answer the user's query respectfully. "
                       "Keep your response concise but profound. Do not make up any shlokas; strictly use the context provided. "
                       "IMPORTANT: The user has selected '{language}' as their preferred language. You MUST reply fluently in {language}, ensuring the translation is culturally nuanced and highly accurate. If the language is Kannada, respond fully in Kannada script."),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{question}")
        ])
        
        # Build Chain
        def format_docs(docs):
            formatted = []
            for d in docs:
                m = d.metadata
                formatted.append(
                    f"Chapter {m['chapter']}, Verse {m['verse']}:\n"
                    f"Sanskrit: {m['sanskrit']}\n"
                    f"Transliteration: {m['transliteration']}\n"
                    f"Translation: {m['translation']}"
                )
            return "\n\n---\n\n".join(formatted)
            
        from operator import itemgetter
        self.chain = (
            {
                "context": itemgetter("question") | self.retriever | format_docs,
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
                
        # Retrieve docs manually to return them alongside the answer
        docs = self.retriever.invoke(query)
        shlokas = [doc.metadata for doc in docs]
        
        # Generate answer
        answer = self.chain.invoke({"question": query, "language": language, "history": history})
        
        return {
            "answer": answer,
            "shlokas": shlokas
        }

if __name__ == "__main__":
    # Test
    groq_key = os.getenv("GROQ_API_KEY", "gsk_...")
    rag = GitaRAG(groq_key)
    res = rag.get_response("I am feeling anxious about my upcoming exams. What should I do?")
    print(res["answer"])
