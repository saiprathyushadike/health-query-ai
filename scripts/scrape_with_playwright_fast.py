import asyncio
import json
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from playwright.async_api import async_playwright
from data_loader import MedicalDataLoader
from rag_system import HealthRAGSystem
from langchain.schema import Document
import aiohttp
import concurrent.futures

class MayoClinicFastScraper:
    def __init__(self, max_concurrent=5):
        self.data_loader = MedicalDataLoader()
        self.scraped_data = []
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    async def scrape_letter_page_fast(self, session, letter):
        """Scrape a single letter page using aiohttp for speed"""
        print(f"Scraping letter {letter}...")
        
        url = f"https://www.mayoclinic.org/diseases-conditions/index?letter={letter}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Use regex to extract URLs quickly
                    import re
                    url_pattern = r'href="([^"]*diseases-conditions/[^"]*/symptoms-causes/[^"]*)"'
                    name_pattern = r'<a[^>]*href="[^"]*diseases-conditions/[^"]*/symptoms-causes/[^"]*"[^>]*>([^<]+)</a>'
                    
                    urls = re.findall(url_pattern, html)
                    names = re.findall(name_pattern, html)
                    
                    diseases = []
                    for i, url in enumerate(urls):
                        if i < len(names):
                            diseases.append({
                                'name': names[i].strip(),
                                'url': f"https://www.mayoclinic.org{url}" if url.startswith('/') else url
                            })
                    
                    print(f"  Found {len(diseases)} diseases for letter {letter}")
                    return diseases
                else:
                    print(f"  Error: HTTP {response.status} for letter {letter}")
                    return []
                    
        except Exception as e:
            print(f"  Error scraping letter {letter}: {e}")
            return []
    
    async def scrape_disease_content_fast(self, session, disease_info):
        """Scrape content from a specific disease page using aiohttp"""
        async with self.semaphore:  # Limit concurrent requests
            url = disease_info['url']
            print(f"Scraping: {disease_info['name']}")
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # Use BeautifulSoup for content extraction
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract title
                        title_elem = soup.find('h1')
                        title = title_elem.get_text().strip() if title_elem else 'Unknown'
                        
                        # Extract content from multiple possible selectors
                        content_selectors = [
                            'div.content',
                            'main',
                            'article',
                            '.content',
                            '[role="main"]',
                            '.main-content'
                        ]
                        
                        content_text = ""
                        for selector in content_selectors:
                            content_elem = soup.select_one(selector)
                            if content_elem:
                                content_text = content_elem.get_text().strip()
                                break
                        
                        # Extract headings for structure
                        headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
                        headings = [h for h in headings if h and len(h) > 0]
                        
                        # Combine content
                        full_content = content_text
                        if headings:
                            full_content += '\n\n' + '\n'.join(headings)
                        
                        if len(full_content.strip()) > 100:
                            return {
                                "title": title,
                                "content": full_content.strip(),
                                "url": url,
                                "name": disease_info['name']
                            }
                        else:
                            print(f"  Insufficient content for {disease_info['name']}")
                            return None
                    else:
                        print(f"  Error: HTTP {response.status} for {disease_info['name']}")
                        return None
                        
            except Exception as e:
                print(f"  Error scraping {disease_info['name']}: {e}")
                return None
    
    async def scrape_all_diseases_fast(self):
        """Scrape all diseases from A-Z using fast parallel processing"""
        import string
        
        # Use aiohttp session for better performance
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=20)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            all_diseases = []
            
            # Scrape all letter pages in parallel
            print("Scraping all letter pages in parallel...")
            letter_tasks = []
            for letter in string.ascii_uppercase:
                task = self.scrape_letter_page_fast(session, letter)
                letter_tasks.append(task)
            
            # Wait for all letter pages to complete
            letter_results = await asyncio.gather(*letter_tasks, return_exceptions=True)
            
            # Collect all diseases
            for result in letter_results:
                if isinstance(result, list):
                    all_diseases.extend(result)
                else:
                    print(f"Error in letter scraping: {result}")
            
            print(f"\nFound {len(all_diseases)} total diseases to scrape")
            
            # Scrape disease content in parallel batches
            print("Scraping disease content in parallel batches...")
            batch_size = 20  # Process 20 diseases at a time
            
            for i in range(0, len(all_diseases), batch_size):
                batch = all_diseases[i:i + batch_size]
                print(f"\nProcessing batch {i//batch_size + 1}/{(len(all_diseases) + batch_size - 1)//batch_size}")
                
                # Create tasks for this batch
                batch_tasks = []
                for disease in batch:
                    task = self.scrape_disease_content_fast(session, disease)
                    batch_tasks.append(task)
                
                # Wait for batch to complete
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                # Collect results
                for result in batch_results:
                    if isinstance(result, dict):
                        self.scraped_data.append(result)
                    elif result is not None:
                        print(f"Error in disease scraping: {result}")
                
                # Small delay between batches to be polite
                await asyncio.sleep(0.5)
        
        print(f"\nSuccessfully scraped {len(self.scraped_data)} diseases")
    
    def save_data(self, filename="mayo_clinic_fast_data.json"):
        """Save scraped data to JSON file"""
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        print(f"Saved data to {data_path}")
    
    def create_documents(self):
        """Convert scraped data to LangChain documents"""
        documents = []
        for item in self.scraped_data:
            doc = Document(
                page_content=item["content"],
                metadata={
                    "title": item["title"],
                    "source": item["url"],
                    "name": item["name"],
                    "type": "mayo_clinic_fast_scraped"
                }
            )
            documents.append(doc)
        
        # Split into chunks
        chunked_docs = self.data_loader.text_splitter.split_documents(documents)
        print(f"Created {len(chunked_docs)} document chunks from {len(self.scraped_data)} diseases")
        return chunked_docs

async def main():
    print("Starting FAST Mayo Clinic scraping...")
    start_time = time.time()
    
    scraper = MayoClinicFastScraper(max_concurrent=10)  # 10 concurrent requests
    
    # Scrape all diseases
    await scraper.scrape_all_diseases_fast()
    
    # Save data
    scraper.save_data()
    
    # Create documents for RAG system
    documents = scraper.create_documents()
    
    # Initialize RAG system
    print("\nInitializing RAG system...")
    rag_system = HealthRAGSystem()
    
    # Add documents to RAG system
    print("Adding documents to RAG system...")
    rag_system.add_documents(documents)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\nScraping and setup complete!")
    print(f"Total diseases processed: {len(scraper.scraped_data)}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per disease: {total_time/len(scraper.scraped_data):.2f} seconds")
    print("You can now use the RAG system to answer health questions.")

if __name__ == "__main__":
    asyncio.run(main()) 