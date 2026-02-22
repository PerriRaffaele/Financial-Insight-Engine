import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate

# --- CONFIGURATION ---
DB_PATH = "./data/vector_db"
MODEL_NAME = "llama3"

def load_rag_chain():
    print("Loading Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Loading Vector DB from {DB_PATH}...")
    vector_db = Chroma(
        persist_directory=DB_PATH, 
        embedding_function=embeddings
    )
    
    print(f"Connecting to Ollama ({MODEL_NAME})...")
    # UPDATED: Using ChatOllama instead of the old Ollama class
    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=0.2
    )

    template = """You are a strict financial analyst. 
    Answer the question based ONLY on the context provided below.
    If the answer is not in the context, say "I cannot find this information".
    
    Context: {context}
    
    Question: {question}
    
    Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 6, "fetch_k": 20}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    print("RAG Pipeline Ready.")
    return qa_chain