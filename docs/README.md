# Health RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that provides accurate, context-aware, and sourced answers to health-related questions using Mayo Clinic's trusted medical knowledge base.

## 🏥 Features

- **Complete Mayo Clinic Database**: 2,235+ diseases and conditions
- **Fast & Accurate**: 31,000+ document chunks for comprehensive coverage
- **Source Attribution**: All answers sourced from Mayo Clinic
- **Free & Open Source**: Uses Ollama (Llama2) and FAISS vector database

## 📁 Project Structure

```
project1/
├── chat_with_rag.py          # Main chatbot interface
├── rag_system.py             # RAG system implementation
├── data_loader.py            # Data processing utilities
├── add_data_fast.py          # Fast data addition script
├── scrape_with_playwright_fast.py  # Fast web scraper
├── mayo_clinic_fast_data.json      # Complete scraped data (21MB)
├── requirements.txt          # Python dependencies
├── chroma_db/               # Vector database storage
│   └── faiss_index/         # FAISS embeddings (73MB)
├── knowledge_base/          # Additional medical data
└── test_files/              # Development and test files
```

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Ollama Server** (if not running):
   ```bash
   ollama serve
   ```

3. **Run the Chatbot**:
   ```bash
   python chat_with_rag.py
   ```

## 💬 Usage

Ask any health-related question:
- "What are the symptoms of diabetes?"
- "How is heart disease treated?"
- "Tell me about cancer prevention"
- "What causes high blood pressure?"

## 🔧 Technical Details

- **Vector Database**: FAISS for fast similarity search
- **Language Model**: Ollama with Llama2
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Data Source**: Mayo Clinic (scraped A-Z diseases & conditions)
- **Total Documents**: 31,121 chunks from 2,235 diseases

## 📊 Data Statistics

- **Diseases Scraped**: 2,235
- **Document Chunks**: 31,121
- **Vector Database Size**: 73MB
- **Raw Data Size**: 21MB
- **Coverage**: Complete Mayo Clinic A-Z index

## 🛠️ Development

Test files and development scripts are stored in `test_files/` directory.

## 📝 License

This project uses Mayo Clinic data for educational purposes. Please respect Mayo Clinic's terms of service. 