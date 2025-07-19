# 🏥 Health Query AI - Easy Installation Guide

Get your own Health Query AI running locally in just a few minutes!

## 🚀 Quick Start (Recommended)

### Option 1: Automated Setup (Easiest)
```bash
# Clone the repository
git clone https://github.com/saiprathyushadike/health-query-ai.git
cd health-query-ai

# Run the automated setup script
python setup.py
```

### Option 2: Manual Setup
```bash
# Clone the repository
git clone https://github.com/saiprathyushadike/health-query-ai.git
cd health-query-ai

# Create virtual environment
python -m venv health-ai-env
source health-ai-env/bin/activate  # On Windows: health-ai-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Download Llama2 model
ollama pull llama2
```

## 🏃‍♂️ Running the Application

### After Setup (Any Method)
```bash
# Option 1: Use the run script
./run.sh                    # Mac/Linux
run.bat                     # Windows

# Option 2: Manual run
source health-ai-env/bin/activate
streamlit run app_concise.py
```

### Access the Application
Open your browser and go to: **http://localhost:8501**

## 📋 System Requirements

- **Python**: 3.9 or higher
- **RAM**: At least 4GB (8GB recommended)
- **Storage**: 5GB free space
- **OS**: macOS, Linux, or Windows
- **Internet**: Required for initial setup

## 🔧 What Gets Installed

- **Python Dependencies**: All required packages from `requirements.txt`
- **Ollama**: Local AI model server
- **Llama2 Model**: 3.8GB language model
- **Virtual Environment**: Isolated Python environment
- **Run Scripts**: Easy startup scripts for your OS

## 🎯 What You Can Do

Once running, you can:
- 🤖 Ask health questions and get AI-powered responses
- 🏥 Access information on 2,235+ diseases and conditions
- 📊 View health statistics and visualizations
- 💡 Learn interesting health facts
- 📚 Explore the project documentation

## ❓ Common Questions

### "How long does setup take?"
- **First time**: 10-15 minutes (includes downloading Llama2 model)
- **Subsequent runs**: 30 seconds

### "Do I need a powerful computer?"
- **Minimum**: 4GB RAM, any modern CPU
- **Recommended**: 8GB+ RAM for better performance

### "Is my data private?"
- **Yes!** Everything runs locally on your computer
- No data is sent to external servers

### "Can I use it offline?"
- **Yes!** Once set up, it works completely offline
- Only needs internet for initial setup

## 🆘 Troubleshooting

### "Port 8501 is already in use"
```bash
# Kill existing processes
lsof -ti:8501 | xargs kill -9
# Or use a different port
streamlit run app_concise.py --server.port 8502
```

### "Ollama not found"
```bash
# Install Ollama manually
curl -fsSL https://ollama.ai/install.sh | sh
# Restart your terminal
```

### "Python version too old"
```bash
# Update Python to 3.9+ from python.org
# Or use conda: conda install python=3.9
```

### "Out of memory"
- Close other applications
- Restart your computer
- Consider using a smaller model

## 🎉 You're Ready!

Once everything is set up, you'll have your own personal health AI assistant running locally on your computer. No subscriptions, no data sharing, just powerful AI health information at your fingertips!

**Happy health querying! 🏥✨** 