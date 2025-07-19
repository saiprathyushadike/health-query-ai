#!/usr/bin/env python3
"""
Health RAG Chatbot - Main Interface
Provides accurate health information using Mayo Clinic knowledge base
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system import HealthRAGSystem

def main():
    print("Loading embedding model: sentence-transformers/all-MiniLM-L6-v2")
    rag_system = HealthRAGSystem()
    print("Welcome to the Health RAG Chatbot! (Type 'exit' to quit)\n")
    
    while True:
        question = input("Ask a health question: ").strip()
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        
        if question:
            print(f"Processing question: '{question}'")
            answer = rag_system.answer_question(question)
            print(f"\nAnswer: {answer}\n")

if __name__ == "__main__":
    main() 