"""
Installation Time Test for ChromaDB

This script will test how long it takes to install ChromaDB and its dependencies.
"""

import time
import subprocess
import sys

def test_installation():
    """Test the installation time for ChromaDB"""
    
    print("="*60)
    print("CHROMADB INSTALLATION TIME TEST")
    print("="*60)
    
    # Test different installation methods
    methods = [
        {
            "name": "ChromaDB with pip",
            "command": [sys.executable, "-m", "pip", "install", "chromadb==0.4.22"]
        },
        {
            "name": "ChromaDB with conda (if available)",
            "command": ["conda", "install", "-c", "conda-forge", "chromadb", "-y"]
        }
    ]
    
    for method in methods:
        print(f"\nTesting: {method['name']}")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            print("Starting installation...")
            result = subprocess.run(
                method['command'],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if result.returncode == 0:
                print(f"✅ SUCCESS! Installation completed in {duration:.2f} seconds ({duration/60:.2f} minutes)")
                print("Installation output:")
                print(result.stdout[-500:])  # Last 500 characters
            else:
                print(f"❌ FAILED! Installation failed after {duration:.2f} seconds")
                print("Error output:")
                print(result.stderr[-500:])  # Last 500 characters
                
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT! Installation took longer than 5 minutes")
        except Exception as e:
            print(f"❌ ERROR: {e}")

def check_system_info():
    """Check system information that might affect installation time"""
    print("\n" + "="*60)
    print("SYSTEM INFORMATION")
    print("="*60)
    
    import platform
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python version: {sys.version}")
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"Available RAM: {memory.available / (1024**3):.2f} GB")
        print(f"Total RAM: {memory.total / (1024**3):.2f} GB")
    except ImportError:
        print("psutil not available - can't check memory")
    
    # Check internet speed (basic test)
    print("\nTesting internet connection...")
    try:
        import requests
        start_time = time.time()
        response = requests.get("https://pypi.org", timeout=10)
        end_time = time.time()
        print(f"Internet test: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Internet test failed: {e}")

if __name__ == "__main__":
    check_system_info()
    test_installation() 