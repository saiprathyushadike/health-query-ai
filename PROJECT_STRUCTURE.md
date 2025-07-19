# 🏥 Health Query AI - Project Structure

## 📁 Organized Folder Structure

```
health-query-ai/
├── 📄 README.md                    # Main project documentation
├── 📄 requirements.txt             # Python dependencies
├── 🏥 app_concise.py              # Main Streamlit application (Production)
├── 📁 src/                        # Core source code
│   ├── 🧠 rag_system.py           # RAG system implementation
│   └── 📊 data_loader.py          # Data processing utilities
├── 📁 apps/                       # Alternative application versions
│   ├── app.py                     # Original web application
│   ├── app_simple.py              # Simplified version
│   └── app_better.py              # Enhanced version
├── 📁 scripts/                    # Utility scripts and tools
│   ├── 🚀 deploy.py               # Deployment automation
│   └── 📁 legacy/                 # Legacy scripts (archived)
│       ├── chat_with_rag.py       # Original CLI chatbot
│       ├── chat_with_rag_fast.py  # Optimized CLI chatbot
│       ├── run_chatbot.py         # Chatbot runner
│       └── requirements_web.txt   # Legacy web dependencies
├── 📁 docs/                       # Documentation
│   └── 📁 technical/              # Technical documentation
│       ├── PROJECT_SUMMARY.md     # Complete project overview
│       └── TECHNOLOGY_STACK.md    # Detailed technology breakdown
├── 📁 data/                       # Data storage and processing
│   ├── 📁 raw/                    # Raw data files
│   │   ├── mayo_clinic_data.json  # Scraped medical data
│   │   └── knowledge_base/        # Additional medical content
│   └── 📁 processed/              # Processed data
│       └── chroma_db/             # Vector database (FAISS)
├── 📁 tests/                      # Testing and validation
│   ├── test_web.py                # Web interface tests
│   └── [legacy test files]        # Additional test files
├── 📁 .streamlit/                 # Streamlit configuration
│   └── config.toml               # Web app settings
└── 📁 ragbot-env/                 # Virtual environment (gitignored)
```

## 🎯 Folder Purposes & Contents

### **📄 Root Level Files**
- **`README.md`**: Main project documentation and setup guide
- **`requirements.txt`**: Complete Python dependency list with descriptions
- **`app_concise.py`**: Production-ready Streamlit application (main entry point)

### **📁 src/ - Core Source Code**
**Purpose**: Contains the main RAG system implementation and core functionality
- **`rag_system.py`**: Complete RAG pipeline with LangChain, Ollama, and FAISS
- **`data_loader.py`**: Document processing, chunking, and data management utilities

### **📁 apps/ - Alternative Application Versions**
**Purpose**: Different iterations of the web application for reference and development
- **`app.py`**: Original web application with basic features
- **`app_simple.py`**: Simplified version for testing
- **`app_better.py`**: Enhanced version with additional features
- **Note**: `app_concise.py` in root is the current production version

### **📁 scripts/ - Utility Scripts and Tools**
**Purpose**: Automation, deployment, and utility scripts
- **`deploy.py`**: One-click deployment automation
- **`legacy/`**: Archived scripts from earlier development phases
  - **`chat_with_rag.py`**: Original CLI chatbot implementation
  - **`chat_with_rag_fast.py`**: Optimized CLI version
  - **`run_chatbot.py`**: Chatbot runner script
  - **`requirements_web.txt`**: Legacy web dependencies

### **📁 docs/ - Documentation**
**Purpose**: Comprehensive project documentation and technical guides
- **`technical/`**: Detailed technical documentation
  - **`PROJECT_SUMMARY.md`**: Complete project overview with achievements
  - **`TECHNOLOGY_STACK.md`**: Detailed breakdown of all technologies used

### **📁 data/ - Data Storage and Processing**
**Purpose**: Organized data management with clear separation of raw and processed data
- **`raw/`**: Original data files before processing
  - **`mayo_clinic_data.json`**: Scraped medical data (2,235+ diseases)
  - **`knowledge_base/`**: Additional medical content and resources
- **`processed/`**: Processed and indexed data
  - **`chroma_db/`**: FAISS vector database with embeddings

### **📁 tests/ - Testing and Validation**
**Purpose**: Test files and validation scripts
- **`test_web.py`**: Web interface functionality tests
- **Additional test files**: Legacy testing scripts and validation tools

### **📁 .streamlit/ - Streamlit Configuration**
**Purpose**: Streamlit web application configuration
- **`config.toml`**: Web app settings, theme, and behavior configuration

## 🚀 Quick Start Guide

### **For Users (Run the Application)**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the main application
streamlit run app_concise.py
```

### **For Developers (Explore the Code)**
```bash
# Core RAG system
src/rag_system.py          # Main RAG implementation
src/data_loader.py         # Data processing utilities

# Alternative versions
apps/app.py               # Original version
apps/app_simple.py        # Simplified version
apps/app_better.py        # Enhanced version

# Documentation
docs/technical/PROJECT_SUMMARY.md    # Project overview
docs/technical/TECHNOLOGY_STACK.md   # Technology details
```

### **For Deployment**
```bash
# Automated deployment
python scripts/deploy.py

# Manual deployment
streamlit run app_concise.py --server.port 8501
```

## 📊 Data Flow

```
Raw Data (data/raw/) 
    ↓
Processing (src/data_loader.py)
    ↓
Vector Database (data/processed/chroma_db/)
    ↓
RAG System (src/rag_system.py)
    ↓
Web Interface (app_concise.py)
```

## 🔧 Development Workflow

### **Adding New Features**
1. **Core Logic**: Add to `src/` directory
2. **Web Interface**: Modify `app_concise.py` or create new version in `apps/`
3. **Scripts**: Add utility scripts to `scripts/`
4. **Tests**: Add test files to `tests/`
5. **Documentation**: Update files in `docs/`

### **Data Management**
- **Raw Data**: Place in `data/raw/`
- **Processed Data**: Store in `data/processed/`
- **Vector Database**: Automatically managed in `data/processed/chroma_db/`

### **Version Control**
- **Production**: `app_concise.py` (root level)
- **Development**: Use `apps/` for different versions
- **Legacy**: Archived in `scripts/legacy/`

## 🎯 Benefits of This Organization

### **📁 Clear Separation of Concerns**
- **Core Logic**: Isolated in `src/`
- **Applications**: Organized in `apps/`
- **Data**: Separated by processing stage
- **Documentation**: Comprehensive and organized

### **🚀 Easy Navigation**
- **Main Entry Point**: `app_concise.py` in root
- **Core Code**: All in `src/` directory
- **Documentation**: Complete guides in `docs/`
- **Legacy Code**: Archived but accessible

### **🔧 Developer Friendly**
- **Modular Structure**: Easy to find and modify components
- **Version History**: Different app versions preserved
- **Clear Dependencies**: Requirements and setup documented
- **Testing**: Organized test structure

### **📚 Educational Value**
- **Learning Path**: From simple to complex versions
- **Documentation**: Complete technical breakdown
- **Best Practices**: Organized project structure
- **Examples**: Multiple implementation approaches

---

**This organized structure makes Health Query AI easy to navigate, maintain, and extend while preserving the complete development history and educational value.** 🏥✨ 