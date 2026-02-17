from src.rag_engine import load_rag_chain
import time

def test_pipeline():
    # Initialize the chain
    qa_chain = load_rag_chain()
    
    # Define a test question relevant to your PDF
    # (Adjust this based on the PDF you downloaded. If it's Apple 2023, this works)
    question = "What were the total net sales for 2023?"
    
    print(f"\n Asking: {question}\n")
    
    start_time = time.time()
    
    # Run the query
    response = qa_chain.invoke({"query": question})
    
    end_time = time.time()
    
    # Print the Result
    print("="*50)
    print(f"Answer (took {end_time - start_time:.2f}s):")
    print(response['result'])
    print("="*50)
    
    # Print Sources (The "Explainability" Feature)
    print("\n Sources Used:")
    for i, doc in enumerate(response['source_documents']):
        print(f"[{i+1}] Page {doc.metadata.get('page', 'N/A')} - {doc.page_content[:100]}...")

if __name__ == "__main__":
    test_pipeline()