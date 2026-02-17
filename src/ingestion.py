import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- CONFIGURATION ---
DATA_PATH = "./data/raw_pdfs"
DB_PATH = "./data/vector_db"

def create_vector_db():
    """
    1. Loads PDFs
    2. Splits them into chunks
    3. Creates embeddings
    4. Saves to ChromaDB
    """
    
    # 1. Load Documents
    print("Loading PDF documents...")
    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, file)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    
    if not documents:
        print("No PDFs found in data/raw_pdfs/")
        return

    print(f"Loaded {len(documents)} pages from PDFs.")

    # 2. Split Text
    # Cut the text into blocks of roughly 1,000 characters.
    # The end of Chunk A is repeated at the start of Chunk B. This ensures context is never lost at the cutting point.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")

    # 3. Initialize Embeddings
    # We use a local model (no API key required) - perfect for privacy.
    print("Initializing Embedding Model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Create and Persist ("save to disk") Vector DB
    print("Creating Vector Database (ChromaDB)...")
    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print(f"Vector Database created at {DB_PATH}")
    print("Ingestion Complete!")

if __name__ == "__main__":
    create_vector_db()