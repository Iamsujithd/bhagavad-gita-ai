import json
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

def build_vector_store():
    data_path = os.path.join(os.path.dirname(__file__), "data", "gita.json")
    index_path = os.path.join(os.path.dirname(__file__), "data", "faiss_index")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        shlokas = json.load(f)
        
    documents = []
    for s in shlokas:
        # We index based on the translation and theme
        content = f"Theme: {s['theme']}\nTranslation: {s['translation']}"
        metadata = {
            "chapter": s["chapter"],
            "verse": s["verse"],
            "sanskrit": s["sanskrit"],
            "transliteration": s["transliteration"],
            "translation": s["translation"],
            "theme": s["theme"]
        }
        documents.append(Document(page_content=content, metadata=metadata))
        
    print("Loading HuggingFace embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Building FAISS index...")
    vector_store = FAISS.from_documents(documents, embeddings)
    
    print(f"Saving FAISS index to {index_path}...")
    vector_store.save_local(index_path)
    print("Done!")

if __name__ == "__main__":
    build_vector_store()
