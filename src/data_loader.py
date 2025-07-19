"""
Data Loader for Medical Documents

This module handles loading and processing medical documents from various sources
including PDFs, text files, and web content. It prepares the data for our RAG system.
"""

import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import json

class MedicalDataLoader:
    """
    A class to load and process medical documents for the RAG system.
    
    This class can:
    - Load documents from files (PDF, TXT)
    - Scrape medical content from websites
    - Split documents into chunks for better retrieval
    - Add metadata to documents
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the data loader.
        
        Args:
            chunk_size: Size of each text chunk (in characters)
            chunk_overlap: Overlap between chunks (in characters)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitter for breaking documents into chunks
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_text_file(self, file_path: str) -> List[Document]:
        """
        Load a text file and convert it to LangChain Documents.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of Document objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            # Create a single document with metadata
            doc = Document(
                page_content=text,
                metadata={
                    "source": file_path,
                    "type": "text_file",
                    "filename": os.path.basename(file_path)
                }
            )
            
            # Split the document into chunks
            return self.text_splitter.split_documents([doc])
            
        except Exception as e:
            print(f"Error loading text file {file_path}: {e}")
            return []
    
    def scrape_medical_content(self, url: str) -> List[Document]:
        """
        Scrape medical content from a website.
        
        Args:
            url: URL to scrape
            
        Returns:
            List of Document objects
        """
        try:
            # Send request to the website
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Create document with metadata
            doc = Document(
                page_content=text,
                metadata={
                    "source": url,
                    "type": "web_scraped",
                    "title": soup.title.string if soup.title else "Unknown"
                }
            )
            
            # Split into chunks
            return self.text_splitter.split_documents([doc])
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
    
    def create_sample_medical_data(self) -> List[Document]:
        """
        Create sample medical documents for testing the RAG system.
        
        Returns:
            List of Document objects with sample medical content
        """
        sample_data = [
            {
                "content": """
                Diabetes is a chronic disease that affects how your body turns food into energy. 
                There are two main types: Type 1 diabetes, where the body doesn't make insulin, 
                and Type 2 diabetes, where the body doesn't use insulin well. Symptoms include 
                increased thirst, frequent urination, and unexplained weight loss. Treatment 
                typically involves medication, diet changes, and regular exercise.
                """,
                "metadata": {
                    "source": "sample_data",
                    "type": "condition_info",
                    "topic": "diabetes",
                    "title": "Diabetes Overview"
                }
            },
            {
                "content": """
                High blood pressure, also called hypertension, is when the force of blood 
                against artery walls is too high. Normal blood pressure is less than 120/80 mmHg. 
                High blood pressure can lead to heart disease, stroke, and kidney problems. 
                Lifestyle changes like reducing salt intake, exercising regularly, and maintaining 
                a healthy weight can help manage blood pressure.
                """,
                "metadata": {
                    "source": "sample_data",
                    "type": "condition_info",
                    "topic": "hypertension",
                    "title": "High Blood Pressure Information"
                }
            },
            {
                "content": """
                Heart disease refers to several types of heart conditions. The most common 
                type is coronary artery disease, which affects blood flow to the heart. 
                Risk factors include smoking, high blood pressure, high cholesterol, and diabetes. 
                Symptoms may include chest pain, shortness of breath, and fatigue. Prevention 
                includes healthy eating, regular exercise, and avoiding tobacco.
                """,
                "metadata": {
                    "source": "sample_data",
                    "type": "condition_info",
                    "topic": "heart_disease",
                    "title": "Heart Disease Overview"
                }
            }
        ]
        
        documents = []
        for item in sample_data:
            doc = Document(
                page_content=item["content"],
                metadata=item["metadata"]
            )
            # Split into smaller chunks
            chunks = self.text_splitter.split_documents([doc])
            documents.extend(chunks)
        
        return documents
    
    def save_documents_to_json(self, documents: List[Document], file_path: str):
        """
        Save documents to a JSON file for later use.
        
        Args:
            documents: List of Document objects
            file_path: Path to save the JSON file
        """
        try:
            data = []
            for doc in documents:
                data.append({
                    "page_content": doc.page_content,
                    "metadata": doc.metadata
                })
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(documents)} documents to {file_path}")
            
        except Exception as e:
            print(f"Error saving documents: {e}")
    
    def load_documents_from_json(self, file_path: str) -> List[Document]:
        """
        Load documents from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of Document objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            documents = []
            for item in data:
                doc = Document(
                    page_content=item["page_content"],
                    metadata=item["metadata"]
                )
                documents.append(doc)
            
            print(f"Loaded {len(documents)} documents from {file_path}")
            return documents
            
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []

# Example usage and testing
if __name__ == "__main__":
    # Create a data loader instance
    loader = MedicalDataLoader()
    
    # Create sample medical data
    print("Creating sample medical data...")
    sample_docs = loader.create_sample_medical_data()
    
    # Save to JSON file
    loader.save_documents_to_json(sample_docs, "knowledge_base/sample_medical_data.json")
    
    print(f"Created {len(sample_docs)} document chunks")
    print("Sample data saved to knowledge_base/sample_medical_data.json") 