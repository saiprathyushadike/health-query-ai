"""
Fast RAG (Retrieval-Augmented Generation) System for Health Chatbot

Optimized version for faster responses
"""

import os
import pickle
import warnings
from typing import List, Dict, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    # Try newer imports first
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_ollama import Ollama
    from langchain_community.vectorstores import FAISS
except ImportError:
    # Fallback to older imports
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.llms import Ollama
    from langchain.vectorstores import FAISS

import re

class FastHealthRAGSystem:
    """
    A fast RAG system optimized for quick health-related responses.
    
    Optimizations:
    - Reduced document retrieval (k=1 instead of k=3)
    - Shorter, more focused prompts
    - Faster LLM settings
    """
    
    def __init__(self, 
                 model_name: str = "llama2",
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 persist_directory: str = "chroma_db"):
        """
        Initialize the fast RAG system.
        """
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        
        # Initialize components
        self._setup_embeddings()
        self._setup_llm()
        self._setup_vectorstore()
    
    def _setup_embeddings(self):
        """Set up the embedding model."""
        print(f"Loading embedding model: {self.embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Embedding model loaded successfully!")
    
    def _setup_llm(self):
        """Set up the language model with optimized settings."""
        try:
            print(f"Connecting to Ollama model: {self.model_name}")
            self.llm = Ollama(
                model=self.model_name,
                temperature=0.1,  # Low temperature for faster, more focused responses
                base_url="http://localhost:11434",
                # Optimized settings for speed
                num_ctx=2048,  # Reduced context window
                num_predict=256,  # Limit response length
                top_k=10,  # Reduce token selection
                top_p=0.9,  # Slightly more focused
                repeat_penalty=1.1  # Reduce repetition
            )
            print("Language model connected successfully!")
        except Exception as e:
            print(f"Warning: Could not connect to Ollama. Error: {e}")
            self.llm = None
    
    def _setup_vectorstore(self):
        """Set up the vector database."""
        print(f"Setting up vector database in: {self.persist_directory}")
        
        os.makedirs(self.persist_directory, exist_ok=True)
        
        faiss_index_path = os.path.join(self.persist_directory, "faiss_index")
        
        if os.path.exists(faiss_index_path):
            print("Loading existing FAISS index...")
            self.vectorstore = FAISS.load_local(faiss_index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print("Creating new FAISS index...")
            self.vectorstore = None
        print("Vector database setup complete!")
        if self.vectorstore is not None:
            self._setup_qa_chain()
    
    def _setup_qa_chain(self):
        """Set up the optimized QA chain."""
        # Shorter, more focused prompt for faster responses
        prompt_template = """Answer this health question based on the context. Keep it concise and accurate.

Context: {context}
Question: {question}

Answer:"""
        
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        if self.llm:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 1}  # Only retrieve 1 document for speed
                ),
                chain_type_kwargs={"prompt": self.prompt},
                return_source_documents=True
            )
        else:
            self.qa_chain = None
            print("QA chain not created - LLM not available")
    
    def add_documents(self, documents: List[Document]):
        """Add documents to the vector database."""
        if not documents:
            print("No documents to add.")
            return
        
        print(f"Adding {len(documents)} documents to the vector database...")
        
        try:
            if self.vectorstore is None:
                self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            else:
                self.vectorstore.add_documents(documents)
            
            faiss_index_path = os.path.join(self.persist_directory, "faiss_index")
            self.vectorstore.save_local(faiss_index_path)
            
            print(f"Successfully added {len(documents)} documents!")
            print(f"Total documents in database: {self.vectorstore.index.ntotal}")
            self._setup_qa_chain()
            
        except Exception as e:
            print(f"Error adding documents: {e}")
    
    def is_greeting(self, question):
        """Check if the question is a greeting."""
        greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
        return any(re.match(rf"^{greet}\\b", question.strip(), re.IGNORECASE) for greet in greetings)

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question with optimized processing."""
        # Quick checks
        if self.is_greeting(question):
            return {
                "answer": "Hello! I'm your health assistant. Ask me any health-related question.",
                "sources": [],
                "error": None
            }

        if len(question.strip().split()) < 3:
            return {
                "answer": "Please ask a more specific health-related question.",
                "sources": [],
                "error": None
            }

        if not hasattr(self, 'qa_chain') or self.qa_chain is None:
            return {
                "answer": "Sorry, the knowledge base is not loaded yet.",
                "sources": [],
                "error": "QA chain not available"
            }

        try:
            print(f"Processing question: '{question}'")
            result = self.qa_chain({"query": question})
            source_docs = result.get("source_documents", [])
            answer = result.get("result", "No answer generated")

            # Quick validation
            if not source_docs or answer.strip().lower() == question.strip().lower():
                return {
                    "answer": "I'm not sure how to answer that. Please ask a health-related question.",
                    "sources": [],
                    "error": None
                }

            sources = [
                {
                    "content": doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in source_docs
            ]

            return {
                "answer": answer,
                "sources": sources,
                "error": None
            }

        except Exception as e:
            print(f"Error generating answer: {e}")
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information."""
        try:
            if self.vectorstore is None:
                count = 0
            else:
                count = self.vectorstore.index.ntotal
            
            return {
                "total_documents": count,
                "embedding_model": self.embedding_model,
                "llm_model": self.model_name,
                "optimization": "fast_mode"
            }
        except Exception as e:
            return {"error": f"Could not retrieve database info: {e}"} 