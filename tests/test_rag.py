"""
Test script for the Health RAG System

This script demonstrates how to:
1. Load sample medical data
2. Initialize the RAG system
3. Add documents to the vector database
4. Ask questions and get answers
"""

from data_loader import MedicalDataLoader
from rag_system import HealthRAGSystem
import time

def test_rag_system():
    """
    Test the complete RAG system workflow.
    """
    print("="*60)
    print("HEALTH RAG SYSTEM TEST")
    print("="*60)
    
    # Step 1: Create sample medical data
    print("\n1. Creating sample medical data...")
    loader = MedicalDataLoader()
    sample_docs = loader.create_sample_medical_data()
    print(f"   Created {len(sample_docs)} document chunks")
    
    # Step 2: Initialize RAG system
    print("\n2. Initializing RAG system...")
    rag_system = HealthRAGSystem()
    
    # Step 3: Add documents to vector database
    print("\n3. Adding documents to vector database...")
    rag_system.add_documents(sample_docs)
    
    # Step 4: Get database info
    print("\n4. Database information:")
    info = rag_system.get_database_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # Step 5: Test questions
    print("\n5. Testing questions...")
    test_questions = [
        "What are the symptoms of diabetes?",
        "How can I manage high blood pressure?",
        "What are the risk factors for heart disease?",
        "What is the normal blood pressure range?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Question {i}: {question}")
        print("   " + "-" * 50)
        
        # Get answer
        result = rag_system.answer_question(question)
        
        # Display answer
        print(f"   Answer: {result['answer']}")
        
        # Display sources
        if result['sources']:
            print(f"   Sources ({len(result['sources'])} documents):")
            for j, source in enumerate(result['sources'], 1):
                print(f"     Source {j}: {source['metadata'].get('title', 'Unknown')}")
                print(f"     Topic: {source['metadata'].get('topic', 'Unknown')}")
        
        if result['error']:
            print(f"   Error: {result['error']}")
        
        print()  # Empty line for readability
        time.sleep(1)  # Small delay between questions
    
    print("="*60)
    print("TEST COMPLETE!")
    print("="*60)

def test_document_search():
    """
    Test document search functionality.
    """
    print("\n" + "="*60)
    print("DOCUMENT SEARCH TEST")
    print("="*60)
    
    # Initialize system
    rag_system = HealthRAGSystem()
    
    # Test search queries
    search_queries = [
        "diabetes symptoms",
        "blood pressure management",
        "heart disease prevention"
    ]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        docs = rag_system.search_documents(query, k=2)
        
        for i, doc in enumerate(docs, 1):
            print(f"  Document {i}:")
            print(f"    Title: {doc.metadata.get('title', 'Unknown')}")
            print(f"    Topic: {doc.metadata.get('topic', 'Unknown')}")
            print(f"    Content preview: {doc.page_content[:100]}...")
            print()

if __name__ == "__main__":
    # Run the main test
    test_rag_system()
    
    # Run document search test
    test_document_search() 