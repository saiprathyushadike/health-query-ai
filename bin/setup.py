#!/usr/bin/env python3
"""
Health Query AI - Automated Setup Script
Makes it easy for anyone to run the application locally
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    print("🔍 Checking Ollama installation...")
    
    # Check if ollama is installed
    if shutil.which("ollama") is None:
        print("❌ Ollama is not installed!")
        print("📥 Installing Ollama...")
        
        system = platform.system().lower()
        if system == "darwin":  # macOS
            if not run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installing Ollama"):
                return False
        elif system == "linux":
            if not run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installing Ollama"):
                return False
        elif system == "windows":
            print("❌ Please install Ollama manually from https://ollama.ai/download")
            return False
        else:
            print(f"❌ Unsupported operating system: {system}")
            return False
    
    # Check if ollama is running
    if not run_command("ollama list", "Checking Ollama status"):
        print("🚀 Starting Ollama service...")
        if not run_command("ollama serve", "Starting Ollama service"):
            return False
    
    # Check if llama2 model is available
    result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
    if "llama2" not in result.stdout:
        print("📥 Downloading Llama2 model (this may take a while)...")
        if not run_command("ollama pull llama2", "Downloading Llama2 model"):
            return False
    
    print("✅ Ollama is ready!")
    return True

def setup_virtual_environment():
    """Set up Python virtual environment"""
    venv_name = "health-ai-env"
    
    if os.path.exists(venv_name):
        print(f"✅ Virtual environment '{venv_name}' already exists!")
        return True
    
    print(f"📦 Creating virtual environment '{venv_name}'...")
    if not run_command(f"python -m venv {venv_name}", "Creating virtual environment"):
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Determine activation command based on OS
    system = platform.system().lower()
    if system == "windows":
        activate_cmd = "health-ai-env\\Scripts\\activate"
        pip_cmd = "health-ai-env\\Scripts\\pip"
    else:
        activate_cmd = "source health-ai-env/bin/activate"
        pip_cmd = "health-ai-env/bin/pip"
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True

def create_run_script():
    """Create a simple run script for users"""
    script_content = """#!/bin/bash
# Health Query AI - Quick Start Script

echo "🏥 Starting Health Query AI..."
echo "📱 Opening browser at http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the application"
echo ""

# Activate virtual environment and run
source health-ai-env/bin/activate
streamlit run app_concise.py
"""
    
    # Create run script for Unix-like systems
    with open("run.sh", "w") as f:
        f.write(script_content)
    
    # Make it executable
    os.chmod("run.sh", 0o755)
    
    # Create Windows batch file
    windows_script = """@echo off
echo 🏥 Starting Health Query AI...
echo 📱 Opening browser at http://localhost:8501
echo ⏹️  Press Ctrl+C to stop the application
echo.

call health-ai-env\\Scripts\\activate
streamlit run app_concise.py
pause
"""
    
    with open("run.bat", "w") as f:
        f.write(windows_script)
    
    print("✅ Created run scripts: run.sh (Unix/Mac) and run.bat (Windows)")

def main():
    """Main setup function"""
    print("🏥 Health Query AI - Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check/Install Ollama
    if not check_ollama():
        print("❌ Ollama setup failed. Please install manually from https://ollama.ai")
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("❌ Virtual environment setup failed!")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed!")
        sys.exit(1)
    
    # Create run scripts
    create_run_script()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Run the application:")
    print("   - On Mac/Linux: ./run.sh")
    print("   - On Windows: run.bat")
    print("   - Or manually: source health-ai-env/bin/activate && streamlit run app_concise.py")
    print("2. Open your browser to: http://localhost:8501")
    print("3. Start asking health questions!")
    print("\n🚀 Enjoy your Health Query AI!")

if __name__ == "__main__":
    main() 