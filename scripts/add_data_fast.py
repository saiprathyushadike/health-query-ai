import json
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import MedicalDataLoader
from rag_system import HealthRAGSystem
from langchain.schema import Document

def load_scraped_data(filename="mayo_clinic_fast_data.json"):
    """Load the scraped data from JSON file"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    print(f"Loading data from {data_path}...")
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} diseases")
    return data

def create_documents_batch(data_loader, scraped_data, batch_size=100):
    """Create documents in batches to avoid memory issues"""
    documents = []
    
    print(f"Creating documents from {len(scraped_data)} diseases...")
    
    for i, item in enumerate(scraped_data):
        if i % 100 == 0:
            print(f"Processing disease {i+1}/{len(scraped_data)}")
            
        doc = Document(
            page_content=item["content"],
            metadata={
                "title": item["title"],
                "source": item["url"],
                "name": item["name"],
                "type": "mayo_clinic_fast_scraped"
            }
        )
        documents.append(doc)
    
    print(f"Created {len(documents)} documents")
    
    # Split into chunks
    print("Splitting documents into chunks...")
    chunked_docs = data_loader.text_splitter.split_documents(documents)
    print(f"Created {len(chunked_docs)} document chunks")
    
    return chunked_docs

def add_documents_batch(rag_system, documents, batch_size=50):
    """Add documents to RAG system in batches"""
    print(f"Adding {len(documents)} documents to RAG system in batches of {batch_size}...")
    
    total_batches = (len(documents) + batch_size - 1) // batch_size
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        print(f"Adding batch {batch_num}/{total_batches} ({len(batch)} documents)...")
        start_time = time.time()
        
        rag_system.add_documents(batch)
        
        end_time = time.time()
        batch_time = end_time - start_time
        print(f"  Batch {batch_num} completed in {batch_time:.2f} seconds")
        
        # Show progress
        progress = (i + len(batch)) / len(documents) * 100
        print(f"  Progress: {progress:.1f}% complete")

def main():
    start_time = time.time()
    
    print("=== Fast Data Addition to RAG System ===")
    
    # Load data
    scraped_data = load_scraped_data()
    
    # Initialize data loader
    data_loader = MedicalDataLoader()
    
    # Create documents
    documents = create_documents_batch(data_loader, scraped_data)
    
    # Initialize RAG system
    print("\nInitializing RAG system...")
    rag_system = HealthRAGSystem()
    
    # Add documents in batches
    add_documents_batch(rag_system, documents, batch_size=50)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n=== Data Addition Complete ===")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Total diseases processed: {len(scraped_data)}")
    print(f"Total document chunks: {len(documents)}")
    print(f"Average time per document: {total_time/len(documents):.3f} seconds")
    print("\nYou can now use the RAG system to answer health questions!")

if __name__ == "__main__":
    main() 