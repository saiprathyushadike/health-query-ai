#!/usr/bin/env python3
"""
Health RAG Chatbot Runner
Simple script to start the chatbot with proper setup
"""

import os
import sys
import subprocess

def check_ollama():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def start_ollama():
    """Start Ollama server"""
    print("🔄 Starting Ollama server...")
    try:
        subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Ollama server started in background")
        return True
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first:")
        print("   curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def main():
    print("🏥 Health RAG Chatbot")
    print("=" * 40)
    
    # Check if Ollama is running
    if not check_ollama():
        print("⚠️  Ollama not running. Attempting to start...")
        if not start_ollama():
            print("❌ Failed to start Ollama. Please start it manually:")
            print("   ollama serve")
            return
    
    print("✅ Ollama is ready!")
    print("\n🚀 Starting chatbot...")
    print("=" * 40)
    
    # Run the main chatbot
    try:
        from chat_with_rag import main as chat_main
        chat_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting chatbot: {e}")

if __name__ == "__main__":
    main() 