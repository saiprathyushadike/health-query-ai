import os
import json
from typing import Dict, List, Any, Optional
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltraFastHealthRAGSystem:
    """
    Ultra-fast RAG system optimized for maximum speed
    Uses smaller model, minimal context, and aggressive optimizations
    """
    
    def __init__(self, model_name: str = "llama2:7b-chat-q4_0"):
        """Initialize the ultra-fast RAG system"""
        self.model_name = model_name
        self.embeddings = None
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None
        
        # Ultra-fast settings
        self.max_context_length = 1024  # Even smaller context
        self.num_docs_to_retrieve = 1   # Only 1 document
        self.max_response_tokens = 256   # Increased for better responses
        self.temperature = 0.1          # Very focused
        self.top_k = 1                  # Only top 1 result
        
        self._setup_system()
    
    def _setup_system(self):
        """Setup the ultra-fast RAG system"""
        try:
            # Load embedding model
            logger.info(f"Loading embedding model: sentence-transformers/all-MiniLM-L6-v2")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}  # Force CPU for speed
            )
            logger.info("Embedding model loaded successfully!")
            
            # Connect to ultra-fast LLM
            logger.info(f"Connecting to Ollama model: {self.model_name}")
            self.llm = Ollama(
                model=self.model_name,
                temperature=self.temperature,
                num_ctx=self.max_context_length,
                num_predict=self.max_response_tokens,
                top_k=self.top_k,
                top_p=0.1,  # Very focused
                repeat_penalty=1.0,  # No repetition
                stop=["\n\n", "Question:", "Answer:", "Human:", "Assistant:"]
            )
            logger.info("Language model connected successfully!")
            
            # Setup vector database
            self._setup_vectorstore()
            
        except Exception as e:
            logger.error(f"Error setting up ultra-fast RAG system: {e}")
            raise
    
    def _setup_vectorstore(self):
        """Setup the vector database with ultra-fast settings"""
        try:
            db_path = "chroma_db"
            logger.info(f"Setting up vector database in: {db_path}")
            
            # Check if FAISS index exists
            faiss_index_path = os.path.join(db_path, "faiss_index")
            if os.path.exists(faiss_index_path):
                logger.info("Loading existing FAISS index...")
                self.vectorstore = FAISS.load_local(
                    faiss_index_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                logger.info("Creating new FAISS index...")
                # Load sample data for ultra-fast testing
                sample_data = self._load_sample_data()
                self.vectorstore = FAISS.from_texts(
                    sample_data, 
                    self.embeddings
                )
                self.vectorstore.save_local(faiss_index_path)
            
            # Create ultra-fast QA chain
            self._create_qa_chain()
            logger.info("Vector database setup complete!")
            
        except Exception as e:
            logger.error(f"Error setting up vector database: {e}")
            raise
    
    def _load_sample_data(self) -> List[str]:
        """Load a small sample of data for ultra-fast testing"""
        sample_texts = [
            "Diabetes is a chronic disease that affects how your body turns food into energy. Symptoms include increased thirst, frequent urination, and blurred vision.",
            "High blood pressure (hypertension) is a common condition that affects the body's arteries. Treatment includes lifestyle changes and medication.",
            "Heart disease refers to several types of heart conditions. The most common type is coronary artery disease. Prevention includes healthy diet and exercise.",
            "Dark circles under the eyes can be caused by fatigue, allergies, aging, or genetics. Treatment includes getting enough sleep (7-9 hours), using cold compresses, applying cucumber slices, using eye creams with vitamin K or retinol, staying hydrated, managing allergies, and avoiding rubbing your eyes. For persistent cases, consider consulting a dermatologist for professional treatments.",
            "Asthma is a condition that affects the airways in the lungs. Symptoms include wheezing, coughing, and shortness of breath.",
            "Arthritis is inflammation of the joints. Common types include osteoarthritis and rheumatoid arthritis. Treatment focuses on pain management.",
            "Migraine is a type of headache that can cause severe pain and other symptoms. Triggers include stress, certain foods, and hormonal changes.",
            "Depression is a mental health disorder characterized by persistent sadness and loss of interest. Treatment includes therapy and medication.",
            "Obesity is a medical condition involving excess body fat. It increases the risk of heart disease, diabetes, and other health problems.",
            "Cancer is a group of diseases characterized by uncontrolled cell growth. Early detection and treatment are crucial for better outcomes."
        ]
        return sample_texts
    
    def _create_qa_chain(self):
        """Create an ultra-fast QA chain with minimal prompt"""
        # Ultra-minimal prompt for speed with context
        template = """Based on the provided context, answer this health question completely and accurately:

Context: {context}
Question: {question}

Provide a complete answer with specific details:"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval chain with ultra-fast settings
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": self.num_docs_to_retrieve,
                    "score_threshold": 0.5  # Only very relevant docs
                }
            ),
            chain_type_kwargs={
                "prompt": prompt,
                "verbose": False
            },
            return_source_documents=False,
            verbose=False
        )
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a health question with ultra-fast processing
        
        Args:
            question (str): The health question to answer
            
        Returns:
            Dict[str, Any]: Answer and metadata
        """
        try:
            logger.info(f"Processing question: '{question}'")
            
            # Ultra-fast processing with minimal overhead
            result = self.qa_chain.run(question)
            
            # Clean up the response
            if isinstance(result, str):
                answer = result.strip()
            else:
                answer = str(result).strip()
            
            # Ensure response is not too long
            if len(answer) > 400:
                answer = answer[:400] + "..."
            
            return {
                "answer": answer,
                "model": self.model_name,
                "context_length": self.max_context_length,
                "docs_retrieved": self.num_docs_to_retrieve,
                "max_tokens": self.max_response_tokens
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "error": True
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the ultra-fast system"""
        return {
            "model": self.model_name,
            "max_context_length": self.max_context_length,
            "num_docs_to_retrieve": self.num_docs_to_retrieve,
            "max_response_tokens": self.max_response_tokens,
            "temperature": self.temperature,
            "optimization_level": "ultra_fast"
        } 