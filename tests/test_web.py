#!/usr/bin/env python3
"""
Test script for the web application components
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_rag_system():
    """Test if the RAG system loads correctly"""
    print("🧪 Testing RAG System...")
    try:
        from rag_system import HealthRAGSystem
        rag = HealthRAGSystem()
        print("✅ RAG system loaded successfully!")
        
        # Test a simple question
        print("🧪 Testing question answering...")
        result = rag.answer_question("What is diabetes?")
        if result:
            print("✅ Question answering works!")
            return True
        else:
            print("❌ Question answering failed")
            return False
            
    except Exception as e:
        print(f"❌ RAG system test failed: {e}")
        return False

def test_imports():
    """Test if all required imports work"""
    print("🧪 Testing imports...")
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully!")
        
        import langchain
        print("✅ LangChain imported successfully!")
        
        import faiss
        print("✅ FAISS imported successfully!")
        
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    print("🏥 Health RAG Chatbot - Web Application Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed")
        return
    
    # Test RAG system
    if not test_rag_system():
        print("❌ RAG system tests failed")
        return
    
    print("\n🎉 All tests passed!")
    print("✅ Web application is ready to run!")
    print("\n🚀 To start the web app, run:")
    print("   streamlit run app.py")
    print("\n🌐 The app will be available at: http://localhost:8501")

if __name__ == "__main__":
    main() 