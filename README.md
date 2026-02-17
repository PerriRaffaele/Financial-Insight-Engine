# Secure Financial Insight Engine (Local RAG)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 📖 Executive Summary

The **Secure Financial Insight Engine** is an end-to-end **Retrieval-Augmented Generation (RAG)** pipeline designed for the analysis of sensitive financial documents (10-Ks, Annual Reports, Internal Memos). 

Unlike standard RAG solutions that rely on external APIs (OpenAI, Anthropic), this system runs **entirely locally** on consumer hardware. It leverages quantized Large Language Models (LLMs) via **Ollama** and local vector stores, ensuring that **no data ever leaves the secure execution environment**. This architecture is specifically designed to meet the strict data privacy and compliance standards of the banking and wealth management sector.

---

## 🚀 Key Features

* **🔒 Zero-Data Leakage:** Full offline capability. Ingestion, embedding generation, and inference happen on-device (Localhost).
* **🧠 Explainable AI (XAI):** Every generated answer includes **strict source citations** (Document Name + Page Number), allowing auditors to verify the model's output.
* **⚡ Hardware Optimized:** Utilizes 4-bit quantization to run 8B parameter models (Llama 3) efficiently on standard RAM/VRAM.
* **🐳 Production Ready:** Fully containerized with **Docker** for consistent deployment across environments.
* **📄 Financial Context Awareness:** Custom chunking strategies optimized for financial tables and dense regulatory text.

---

## 🛠️ Tech Stack

| Component | Technology | Reason for Choice |
| :--- | :--- | :--- |
| **LLM Inference** | [Ollama](https://ollama.com) (Llama 3 / Mistral) | Low-latency local inference with quantization support. |
| **Orchestration** | [LangChain](https://www.langchain.com/) | Robust framework for chaining retrieval and generation steps. |
| **Vector Database** | [ChromaDB](https://www.trychroma.com/) | Open-source, persistent local vector storage. |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) | High speed/accuracy ratio for semantic search on CPU. |
| **Frontend** | [Streamlit](https://streamlit.io/) | Rapid prototyping of interactive data apps. |
| **Deployment** | Docker & Docker Compose | Reproducibility and environment isolation. |

---

## 🏗️ Architecture

*TODO: Place a diagram here later. For now, we describe the flow.*

1.  **Ingestion:** PDFs are loaded and split into semantic chunks (overlapping windows) to preserve financial context.
2.  **Embedding:** Chunks are converted to vector embeddings locally using HuggingFace models.
3.  **Storage:** Vectors are stored in a persistent ChromaDB instance.
4.  **Retrieval:** User queries trigger a semantic search to find the top-k most relevant document chunks.
5.  **Generation:** The strictly prompted Local LLM synthesizes an answer using *only* the retrieved context.

---

## 🗺️ Development Roadmap & Status

This project follows an iterative development path, moving from core logic to production-grade deployment.

### Phase 1: Foundation & Local LLM Setup ✅
- [x] Set up Python environment and Git repository.
- [x] Configure **Ollama** for local model serving (Llama 3).
- [x] Verify local inference capabilities via terminal.
- [x] Establish basic connection between Python (`langchain`) and Ollama.

### Phase 2: Data Ingestion Pipeline (ETL) 🚧

*Note: Used the "Apple (AAPL) 2023 10-K Annual Report" as raw_pdf*

- [x] **PDF Loading:** Implement `PyPDFLoader` to handle complex financial documents.
- [x] **Chunking Strategy:** Apply `RecursiveCharacterTextSplitter` with overlap to maintain context across line breaks.
- [x] **Vector Storage:** Set up **ChromaDB** to store embeddings locally.
- [x] **Embedding Generation:** Process raw text into vectors using `HuggingFaceEmbeddings`.

### Phase 3: RAG Logic & Retrieval ⏳
- [ ] **Retrieval Chain:** Build the logic to fetch the top-k most relevant chunks for a query.
- [ ] **Prompt Engineering:** Design a "Strict Financial Analyst" system prompt to minimize hallucinations.
- [ ] **Citation Logic:** Engineer the return object to include source metadata (Page numbers/Filenames).

### Phase 4: User Interface (Frontend) ⏳
- [ ] **Streamlit Setup:** Initialize the web app structure.
- [ ] **File Uploader:** Allow users to upload new PDF reports dynamically.
- [ ] **Chat Interface:** Build the Q&A loop with history memory.
- [ ] **Source Display:** Visual component to show the "Why" behind the answer (Explainability).

### Phase 5: Containerization & Optimization ⏳
- [ ] **Dockerization:** Write `Dockerfile` and `docker-compose.yml`.
- [ ] **Network Isolation:** Ensure containers communicate without external internet access.
- [ ] **Performance Tuning:** Optimize chunk sizes and retrieval parameters (`k` value) for speed/accuracy balance.

## 💻 Installation & Usage

### Prerequisites
* **Docker Desktop** installed.
* **Ollama** installed on your host machine (for local model serving).

### Method 1: Quick Start (Docker)

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/financial-rag-system.git](https://github.com/YOUR_USERNAME/financial-rag-system.git)
cd financial-rag-system

# 2. Build and Run the Container
docker-compose up --build

