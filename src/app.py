import os
import shutil
import streamlit as st
from rag_engine import load_rag_chain
from ingestion import create_vector_db

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Financial Insight Engine",
    page_icon="💰",
    layout="wide"
)

# --- HEADER ---
st.title("Financial Insight Engine")
st.markdown("### Private, Local, & Explainable AI for Finance")
st.markdown("---")

# --- INITIALIZE SESSION STATE (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR (System Status & Upload) ---
with st.sidebar:
    st.header("1. Upload Documents")
    # CHANGED: Added accept_multiple_files=True
    uploaded_files = st.file_uploader("Upload PDF Reports", type="pdf", accept_multiple_files=True)

    # --- DYNAMIC UPLOAD LOGIC ---
    if uploaded_files:
        # Get a list of current file names
        file_names = [f.name for f in uploaded_files]

        # Check if the exact SET of uploaded files has changed
        if "current_files" not in st.session_state or set(st.session_state.current_files) != set(file_names):
            with st.spinner(f"Ingesting {len(uploaded_files)} document(s)... This may take a few minutes."):

                # 1. Clean up old PDFs
                if os.path.exists("./data/raw_pdfs"):
                    for f in os.listdir("./data/raw_pdfs"):
                        os.remove(os.path.join("./data/raw_pdfs", f))
                else:
                    os.makedirs("./data/raw_pdfs", exist_ok=True)

                # 2. Clean up old Vector DB
                if os.path.exists("./data/vector_db"):
                    shutil.rmtree("./data/vector_db")
                os.makedirs("./data/vector_db", exist_ok=True)

                # 3. Save ALL new uploaded PDFs
                for uploaded_file in uploaded_files:
                    file_path = os.path.join("./data/raw_pdfs", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                # 4. Trigger the ETL Pipeline!
                # It will automatically loop through all files in the raw_pdfs folder
                create_vector_db()

                # 5. Reload the Brain & clear old chat history
                st.session_state.rag_chain = load_rag_chain()
                st.session_state.current_files = file_names
                st.session_state.messages = []

            st.success(f"Successfully loaded {len(uploaded_files)} document(s)!")
# --- CHAT INTERFACE ---

# Graceful stop if no files are loaded
if "current_files" not in st.session_state or not st.session_state.current_files:
    st.warning("Please upload at least one PDF document in the sidebar to begin.")
    st.stop()

# 1. Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. User Input Field
if prompt := st.chat_input("Ask a question about the uploaded reports..."):

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents & verifying citations..."):
            try:
                # Run the RAG Chain
                response = st.session_state.rag_chain.invoke({"query": prompt})
                answer = response['result']
                sources = response['source_documents']

                # Display the Answer
                st.markdown(answer)

                # Append to history
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # --- CITATION BLOCK ---
                with st.expander("Evidence & Citations"):
                    for i, doc in enumerate(sources):
                        page_num = doc.metadata.get('page', 'Unknown')
                        # Extract the filename from the source path
                        source_path = doc.metadata.get('source', 'Unknown')
                        source_file = os.path.basename(source_path)

                        st.markdown(f"**Source {i + 1}** ({source_file} - Page {page_num})")
                        st.caption(f"...{doc.page_content[:300]}...")
                        st.markdown("---")

            except Exception as e:
                st.error(f"Error: {str(e)}")