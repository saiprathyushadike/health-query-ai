import requests
import time
import json
import os
import re
from bs4 import BeautifulSoup
from data_loader import MedicalDataLoader
from rag_system import HealthRAGSystem

# Constants
BASE_URL = "https://www.mayoclinic.org"
INDEX_URL = "https://www.mayoclinic.org/diseases-conditions/index?letter={}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_json_data(html_content):
    """Extract URLs directly from the HTML using regex"""
    # Look for URLs that match the symptoms-causes pattern
    url_pattern = r'"url":\s*"([^"]*diseases-conditions/[^"]*/symptoms-causes/[^"]*)"'
    matches = re.findall(url_pattern, html_content)
    
    if matches:
        print(f"  Found {len(matches)} URLs using direct pattern matching")
        return matches
    else:
        print("  No URLs found using direct pattern matching")
        return []

def get_condition_urls():
    """Get all condition URLs using the embedded JSON data approach"""
    print("Scraping Mayo Clinic index for all condition URLs (extracting from embedded JSON)...")
    all_condition_links = set()
    
    for letter in string.ascii_uppercase:
        url = INDEX_URL.format(letter)
        print(f"Scraping letter page: {url}")
        
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            
            # Extract URLs from embedded JSON
            urls = extract_json_data(resp.text)
            print(f"  Found {len(urls)} disease links on letter {letter} page.")
            
            for url in urls:
                if url.startswith("/"):
                    full_url = BASE_URL + url
                else:
                    full_url = url
                all_condition_links.add(full_url)
                print(f"    Added: {full_url}")
            
            time.sleep(0.5)  # Be polite to the server
            
        except Exception as e:
            print(f"  Error scraping letter {letter}: {e}")
            continue
    
    print(f"Found {len(all_condition_links)} unique symptoms-causes URLs.")
    return list(all_condition_links)

def scrape_condition_content(url):
    """Scrape content from a specific condition page"""
    try:
        print(f"Scraping: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        
        # Extract the main content
        content_div = soup.find("div", class_="content")
        if not content_div:
            print(f"  No content div found for {url}")
            return None
            
        # Get the title
        title_elem = soup.find("h1")
        title = title_elem.text.strip() if title_elem else "Unknown Condition"
        
        # Get all text content
        content_text = content_div.get_text(separator=' ', strip=True)
        
        if not content_text or len(content_text) < 100:
            print(f"  Insufficient content for {url}")
            return None
            
        return {
            "title": title,
            "content": content_text,
            "url": url
        }
        
    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return None

def main():
    print("Starting comprehensive Mayo Clinic scraping...")
    
    # Get all condition URLs
    condition_urls = get_condition_urls()
    
    if not condition_urls:
        print("No condition URLs found. Exiting.")
        return
    
    print(f"\nFound {len(condition_urls)} conditions to scrape.")
    
    # Scrape content from each URL
    scraped_data = []
    for i, url in enumerate(condition_urls, 1):
        print(f"\nProgress: {i}/{len(condition_urls)}")
        content = scrape_condition_content(url)
        if content:
            scraped_data.append(content)
        time.sleep(1)  # Be polite to the server
    
    print(f"\nSuccessfully scraped {len(scraped_data)} conditions.")
    
    # Save scraped data
    output_file = "mayo_clinic_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    print(f"Saved scraped data to {output_file}")
    
    # Initialize data loader and RAG system
    print("\nInitializing RAG system...")
    data_loader = MedicalDataLoader()
    rag_system = HealthRAGSystem()
    
    # Add scraped data to the knowledge base
    print("Adding scraped data to knowledge base...")
    documents = []
    for item in scraped_data:
        # Create document format expected by the data loader
        from langchain.schema import Document
        doc = Document(
            page_content=item["content"],
            metadata={
                "title": item["title"],
                "source": item["url"],
                "type": "mayo_clinic_scraped"
            }
        )
        documents.append(doc)
    
    # Split documents into chunks
    chunked_docs = data_loader.text_splitter.split_documents(documents)
    print(f"Created {len(chunked_docs)} document chunks from {len(scraped_data)} conditions")
    
    # Save to vector database
    print("Saving to vector database...")
    data_loader.save_documents_to_json(chunked_docs, "mayo_clinic_chunks.json")
    
    # Add documents to RAG system
    print("Adding documents to RAG system...")
    rag_system.add_documents(chunked_docs)
    
    print("\nScraping and setup complete!")
    print(f"Total conditions processed: {len(scraped_data)}")
    print("You can now use the RAG system to answer health questions.")

if __name__ == "__main__":
    import string
    main() 