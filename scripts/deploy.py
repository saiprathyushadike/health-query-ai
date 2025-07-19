#!/usr/bin/env python3
"""
Health RAG Chatbot - Deployment Script
Easy deployment and configuration for the web application
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

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
        time.sleep(3)  # Wait for server to start
        return True
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first:")
        print("   curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import streamlit
        import langchain
        import faiss
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting Streamlit application...")
    try:
        # Set environment variables for better performance
        env = os.environ.copy()
        env['STREAMLIT_SERVER_PORT'] = '8501'
        env['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
        env['STREAMLIT_SERVER_HEADLESS'] = 'true'
        
        # Run streamlit
        process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--server.headless', 'true'
        ], env=env)
        
        return process
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return None

def main():
    print("🏥 Health RAG Chatbot - Deployment")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("Installing dependencies...")
        if not install_dependencies():
            return
        print("✅ Dependencies installed!")
    
    # Check Ollama
    if not check_ollama():
        print("Starting Ollama...")
        if not start_ollama():
            return
        print("✅ Ollama started!")
    else:
        print("✅ Ollama is running!")
    
    # Start Streamlit
    process = run_streamlit()
    if not process:
        return
    
    print("✅ Streamlit application started!")
    print("\n🌐 Opening web browser...")
    print("📱 The application will be available at: http://localhost:8501")
    
    # Open browser
    try:
        webbrowser.open('http://localhost:8501')
    except:
        print("Please open your browser and go to: http://localhost:8501")
    
    print("\n🔄 Application is running...")
    print("Press Ctrl+C to stop the application")
    
    try:
        # Keep the application running
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping application...")
        process.terminate()
        process.wait()
        print("✅ Application stopped!")

if __name__ == "__main__":
    main() 