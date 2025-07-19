"""
Script to add real medical data to the RAG bot knowledge base.
- Scrapes a trusted health page (e.g., Mayo Clinic)
- Saves the processed chunks to the knowledge base
- Optionally adds them to the vector database
"""

from data_loader import MedicalDataLoader
from rag_system import HealthRAGSystem

# List of Mayo Clinic URLs to scrape
URLS = [
    "https://www.mayoclinic.org/diseases-conditions/diabetes/symptoms-causes/syc-20371444",
    "https://www.mayoclinic.org/diseases-conditions/hypertension/symptoms-causes/syc-20373410",
    "https://www.mayoclinic.org/diseases-conditions/heart-disease/symptoms-causes/syc-20353118",
    "https://www.mayoclinic.org/diseases-conditions/asthma/symptoms-causes/syc-20369653",
    # Add more URLs as needed
]

if __name__ == "__main__":
    loader = MedicalDataLoader()
    all_docs = []
    for url in URLS:
        print(f"Scraping: {url}")
        docs = loader.scrape_medical_content(url)
        print(f"  -> {len(docs)} chunks")
        all_docs.extend(docs)
    print(f"Total chunks scraped: {len(all_docs)}")

    # Save all to a single JSON file
    loader.save_documents_to_json(all_docs, "knowledge_base/mayo_clinic_all.json")
    print("Saved all chunks to knowledge_base/mayo_clinic_all.json")

    # Add to vector database
    rag = HealthRAGSystem()
    rag.add_documents(all_docs)
    print("Added all chunks to the vector database!") 