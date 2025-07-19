#!/usr/bin/env python3
"""
Health Query AI - Demo Script
Test the system with predefined health questions
"""

import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def run_demo():
    """Run a demo of the Health Query AI system"""
    print("🏥 Health Query AI - Demo Mode")
    print("=" * 50)
    
    try:
        from rag_system import HealthRAGSystem
        
        print("🔄 Loading RAG system...")
        rag_system = HealthRAGSystem()
        print("✅ RAG system loaded successfully!")
        
        # Demo questions
        demo_questions = [
            "What are the symptoms of diabetes?",
            "How to manage high blood pressure?",
            "What causes heart disease?",
            "Treatment options for COVID-19"
        ]
        
        print("\n🎯 Running demo questions...")
        print("=" * 50)
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n❓ Question {i}: {question}")
            print("-" * 40)
            
            start_time = time.time()
            
            try:
                response = rag_system.query(question)
                end_time = time.time()
                
                print(f"🤖 Response ({end_time - start_time:.2f}s):")
                print(response)
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("\n" + "=" * 50)
            time.sleep(1)  # Brief pause between questions
        
        print("\n🎉 Demo completed!")
        print("\n💡 Try the web interface:")
        print("   streamlit run app_concise.py")
        print("   Then open: http://localhost:8501")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you've run the setup script first:")
        print("   python setup.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check that Ollama is running and Llama2 model is available")

if __name__ == "__main__":
    run_demo() 