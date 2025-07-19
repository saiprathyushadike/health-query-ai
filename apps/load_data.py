#!/usr/bin/env python3
"""
Load Medical Data into RAG System
Loads the existing Mayo Clinic data into the Health Query AI system
"""

import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def load_mayo_clinic_data():
    """Load Mayo Clinic data from JSON file"""
    print("🏥 Loading Mayo Clinic medical data...")
    
    # Path to the Mayo Clinic data
    data_path = "data/raw/mayo_clinic_fast_data.json"
    
    if not os.path.exists(data_path):
        print(f"❌ Data file not found: {data_path}")
        return None
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} medical entries from Mayo Clinic data")
        return data
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def convert_to_documents(data):
    """Convert JSON data to LangChain Documents"""
    from langchain.schema import Document
    
    documents = []
    
    for item in data:
        # Extract content and metadata
        content = item.get('content', '')
        title = item.get('title', 'Unknown')
        url = item.get('url', '')
        
        if content.strip():  # Only add if there's actual content
            doc = Document(
                page_content=content,
                metadata={
                    "source": url,
                    "title": title,
                    "type": "mayo_clinic",
                    "topic": title.lower().replace(' ', '_')
                }
            )
            documents.append(doc)
    
    print(f"✅ Converted {len(documents)} documents")
    return documents

def main():
    """Main function to load data into RAG system"""
    print("🏥 Health Query AI - Data Loading Script")
    print("=" * 50)
    
    # Load the Mayo Clinic data
    data = load_mayo_clinic_data()
    if not data:
        print("❌ Failed to load data")
        return
    
    # Convert to documents
    documents = convert_to_documents(data)
    if not documents:
        print("❌ No documents to add")
        return
    
    # Initialize RAG system
    try:
        from rag_system import HealthRAGSystem
        
        print("🔄 Initializing RAG system...")
        rag_system = HealthRAGSystem()
        
        # Add documents to the system
        print(f"📚 Adding {len(documents)} documents to the knowledge base...")
        rag_system.add_documents(documents)
        
        print("✅ Data loading completed successfully!")
        print(f"📊 Total documents in database: {rag_system.vectorstore.index.ntotal}")
        
        # Test the system
        print("\n🧪 Testing the system...")
        test_question = "What are the symptoms of diabetes?"
        response = rag_system.answer_question(test_question)
        
        print(f"❓ Test question: {test_question}")
        print(f"🤖 Response: {response.get('answer', 'No answer')[:200]}...")
        
        print("\n🎉 Health Query AI is now ready to use!")
        print("💡 Run: streamlit run app_concise.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure Ollama is running: ollama serve")

if __name__ == "__main__":
    main() 