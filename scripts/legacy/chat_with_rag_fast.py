#!/usr/bin/env python3
"""
Health RAG Chatbot - Fast Version
Optimized for faster loading and better performance
"""

import sys
import os
import warnings
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Suppress deprecation warnings for faster loading
warnings.filterwarnings("ignore", category=DeprecationWarning)

from rag_system import HealthRAGSystem

def main():
    print("🏥 Health RAG Chatbot - Fast Version")
    print("=" * 50)
    print("Loading components...")
    
    # Initialize RAG system (this will show progress)
    rag_system = HealthRAGSystem()
    
    print("\n✅ System ready!")
    print("Welcome to the Health RAG Chatbot! (Type 'exit' to quit)")
    print("=" * 50)
    
    while True:
        try:
            question = input("\nAsk a health question: ").strip()
            if question.lower() == 'exit':
                print("Goodbye!")
                break
            
            if question:
                print(f"Processing: '{question}'")
                result = rag_system.answer_question(question)
                
                # Extract just the answer for cleaner output
                if isinstance(result, dict) and 'answer' in result:
                    answer = result['answer']
                else:
                    answer = str(result)
                
                print(f"\nAnswer: {answer}\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main() 