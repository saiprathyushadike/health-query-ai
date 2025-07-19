"""
RAG (Retrieval-Augmented Generation) System for Health Chatbot

This module implements the core RAG functionality:
1. Document embedding and storage in vector database
2. Semantic search and retrieval
3. Answer generation with source citations
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

class HealthRAGSystem:
    """
    A RAG system specifically designed for health-related questions.
    
    This system:
    - Stores medical documents in a vector database
    - Retrieves relevant information based on user questions
    - Generates accurate, sourced answers
    """
    
    def __init__(self, 
                 model_name: str = "llama2",
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 persist_directory: str = "chroma_db"):
        """
        Initialize the RAG system.
        
        Args:
            model_name: Name of the Ollama model to use
            embedding_model: HuggingFace model for creating embeddings
            persist_directory: Directory to store the vector database
        """
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        
        # Initialize components
        self._setup_embeddings()
        self._setup_llm()
        self._setup_vectorstore()
        # self._setup_qa_chain() # <-- REMOVE this line
    
    def _setup_embeddings(self):
        """
        Set up the embedding model for converting text to vectors.
        
        Embeddings are mathematical representations of text that capture meaning.
        Similar texts will have similar embeddings, allowing us to find relevant documents.
        """
        print(f"Loading embedding model: {self.embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': 'cpu'},  # Use CPU for compatibility
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Embedding model loaded successfully!")
    
    def _setup_llm(self):
        """
        Set up the language model for generating answers.
        
        We use Ollama with Llama2 as a free alternative to OpenAI.
        """
        try:
            print(f"Connecting to Ollama model: {self.model_name}")
            self.llm = Ollama(
                model=self.model_name,
                temperature=0.1,  # Low temperature for more focused answers
                base_url="http://localhost:11434"  # Default Ollama URL
            )
            print("Language model connected successfully!")
        except Exception as e:
            print(f"Warning: Could not connect to Ollama. Error: {e}")
            print("Please make sure Ollama is running and the model is installed.")
            print("You can install it with: ollama pull llama2")
            self.llm = None
    
    def _setup_vectorstore(self):
        """
        Set up the vector database for storing and retrieving documents.
        
        FAISS is a fast, efficient vector database that stores document embeddings.
        """
        print(f"Setting up vector database in: {self.persist_directory}")
        
        # Create the directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Check if we have existing FAISS index
        faiss_index_path = os.path.join(self.persist_directory, "faiss_index")
        
        if os.path.exists(faiss_index_path):
            print("Loading existing FAISS index...")
            self.vectorstore = FAISS.load_local(faiss_index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print("Creating new FAISS index...")
            self.vectorstore = None
        print("Vector database setup complete!")
        if self.vectorstore is not None:
            self._setup_qa_chain()  # Only set up QA chain if vectorstore exists
    
    def _setup_qa_chain(self):
        """
        Set up the question-answering chain that combines retrieval and generation.
        """
        # Create a custom prompt template for health-related questions
        prompt_template = """You are a helpful medical information assistant. Use the following context to answer the user's question. 
        If you cannot answer the question based on the context, say "I don't have enough information to answer that question."
        
        Always provide accurate, helpful information and cite your sources when possible.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create the QA chain
        if self.llm:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",  # Simple chain that stuffs all context into prompt
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}  # Retrieve top 3 most relevant documents
                ),
                chain_type_kwargs={"prompt": self.prompt},
                return_source_documents=True  # Return source documents for citations
            )
        else:
            self.qa_chain = None
            print("QA chain not created - LLM not available")
    
    def add_documents(self, documents: List[Document]):
        """
        Add documents to the vector database.
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            print("No documents to add.")
            return
        
        print(f"Adding {len(documents)} documents to the vector database...")
        
        try:
            # Create or update FAISS index
            if self.vectorstore is None:
                # First time adding documents - create new index
                self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            else:
                # Add to existing index
                self.vectorstore.add_documents(documents)
            
            # Save the index
            faiss_index_path = os.path.join(self.persist_directory, "faiss_index")
            self.vectorstore.save_local(faiss_index_path)
            
            print(f"Successfully added {len(documents)} documents!")
            print(f"Total documents in database: {self.vectorstore.index.ntotal}")
            self._setup_qa_chain()  # <-- ADD this line here
            
        except Exception as e:
            print(f"Error adding documents: {e}")
    
    def search_documents(self, query: str, k: int = 3) -> List[Document]:
        """
        Search for relevant documents based on a query.
        
        Args:
            query: The search query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        try:
            print(f"Searching for documents related to: '{query}'")
            
            # Search the vector database
            docs = self.vectorstore.similarity_search(query, k=k)
            
            print(f"Found {len(docs)} relevant documents")
            return docs
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def is_greeting(self, question):
        greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
        return any(re.match(rf"^{greet}\\b", question.strip(), re.IGNORECASE) for greet in greetings)

    def answer_question(self, question: str) -> Dict[str, Any]:
        # 1. Greeting detection
        if self.is_greeting(question):
            return {
                "answer": "Hello! I'm your health assistant. Ask me any health-related question.",
                "sources": [],
                "error": None
            }

        # 2. Short or generic question fallback
        if len(question.strip().split()) < 3:
            return {
                "answer": "Please ask a more specific health-related question.",
                "sources": [],
                "error": None
            }

        # Check if qa_chain exists and is set up
        if not hasattr(self, 'qa_chain') or self.qa_chain is None:
            return {
                "answer": "Sorry, the knowledge base is not loaded yet. Please add documents to the database.",
                "sources": [],
                "error": "QA chain not available"
            }

        try:
            print(f"Processing question: '{question}'")
            result = self.qa_chain({"query": question})
            source_docs = result.get("source_documents", [])
            answer = result.get("result", "No answer generated")

            # Fallback if answer is too generic or just repeats the question
            if not source_docs or answer.strip().lower() == question.strip().lower():
                return {
                    "answer": "I'm not sure how to answer that. Please ask a health-related question.",
                    "sources": [],
                    "error": None
                }

            sources = [
                {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
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
                "answer": f"Sorry, I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get information about the current state of the vector database.
        
        Returns:
            Dictionary with database statistics
        """
        try:
            if self.vectorstore is None:
                count = 0
            else:
                count = self.vectorstore.index.ntotal
            
            return {
                "total_documents": count,
                "embedding_model": self.embedding_model,
                "llm_model": self.model_name,
                "persist_directory": self.persist_directory,
                "vectorstore_type": "FAISS"
            }
        except Exception as e:
            return {
                "error": f"Could not retrieve database info: {e}"
            }
    
    def clear_database(self):
        """
        Clear all documents from the vector database.
        """
        try:
            print("Clearing vector database...")
            # Remove the FAISS index files
            faiss_index_path = os.path.join(self.persist_directory, "faiss_index")
            if os.path.exists(faiss_index_path):
                import shutil
                shutil.rmtree(faiss_index_path)
            
            # Reset vectorstore
            self.vectorstore = None
            print("Database cleared successfully!")
        except Exception as e:
            print(f"Error clearing database: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Create the RAG system
    print("Initializing Health RAG System...")
    rag_system = HealthRAGSystem()
    
    # Test the system
    print("\n" + "="*50)
    print("RAG SYSTEM TEST")
    print("="*50)
    
    # Get database info
    info = rag_system.get_database_info()
    print(f"Database Info: {info}")
    
    # Test a sample question
    test_question = "What are the symptoms of diabetes?"
    print(f"\nTesting question: {test_question}")
    
    result = rag_system.answer_question(test_question)
    print(f"Answer: {result['answer']}")
    
    if result['sources']:
        print(f"Sources: {len(result['sources'])} documents found")
        for i, source in enumerate(result['sources'], 1):
            print(f"Source {i}: {source['metadata']}") 