import asyncio
import json
import time
from playwright.async_api import async_playwright
from data_loader import MedicalDataLoader
from rag_system import HealthRAGSystem
from langchain.schema import Document

class MayoClinicPlaywrightScraper:
    def __init__(self):
        self.data_loader = MedicalDataLoader()
        self.scraped_data = []
        
    async def scrape_letter_page(self, page, letter):
        """Scrape a single letter page to get all disease URLs"""
        print(f"Scraping letter {letter}...")
        
        url = f"https://www.mayoclinic.org/diseases-conditions/index?letter={letter}"
        
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # Wait a bit for content to load
            await asyncio.sleep(3)
            
            # Extract all disease links
            diseases = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('a[href*="/diseases-conditions/"][href*="/symptoms-causes/"]');
                    return Array.from(links).map(link => ({
                        name: link.textContent.trim(),
                        url: link.href
                    }));
                }
            """)
            
            print(f"  Found {len(diseases)} diseases for letter {letter}")
            return diseases
            
        except Exception as e:
            print(f"  Error scraping letter {letter}: {e}")
            return []
    
    async def scrape_disease_content(self, page, disease_info):
        """Scrape content from a specific disease page"""
        url = disease_info['url']
        print(f"Scraping disease content: {disease_info['name']}")
        
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # Wait a bit for content to load
            await asyncio.sleep(2)
            
            # Extract page content
            content = await page.evaluate("""
                () => {
                    // Get title
                    const title = document.querySelector('h1');
                    const titleText = title ? title.textContent.trim() : 'Unknown';
                    
                    // Get main content
                    const contentSelectors = [
                        'div.content',
                        'main',
                        'article',
                        '.content',
                        '[role="main"]'
                    ];
                    
                    let contentText = '';
                    for (const selector of contentSelectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            contentText = element.textContent.trim();
                            break;
                        }
                    }
                    
                    // Get all headings for structure
                    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'))
                        .map(h => h.textContent.trim())
                        .filter(text => text.length > 0);
                    
                    return {
                        title: titleText,
                        content: contentText,
                        headings: headings
                    };
                }
            """)
            
            # Combine content
            full_content = content['content']
            if content['headings']:
                full_content += '\n\n' + '\n'.join(content['headings'])
            
            if len(full_content.strip()) > 100:  # Only save if we have substantial content
                return {
                    "title": content['title'],
                    "content": full_content.strip(),
                    "url": url,
                    "name": disease_info['name']
                }
            else:
                print(f"  Insufficient content for {disease_info['name']}")
                return None
                
        except Exception as e:
            print(f"  Error scraping {disease_info['name']}: {e}")
            return None
    
    async def scrape_all_diseases(self):
        """Scrape all diseases from A-Z"""
        import string
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set user agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            all_diseases = []
            
            # Scrape all letters A-Z
            test_letters = string.ascii_uppercase  # All letters A-Z
            
            # Scrape all letter pages to get disease URLs
            for letter in test_letters:
                diseases = await self.scrape_letter_page(page, letter)
                all_diseases.extend(diseases)
                await asyncio.sleep(1)  # Be polite to the server
            
            print(f"\nFound {len(all_diseases)} total diseases to scrape")
            
            # Scrape content from ALL disease pages
            test_diseases = all_diseases  # No limit - scrape everything
            for i, disease in enumerate(test_diseases, 1):
                print(f"\nProgress: {i}/{len(test_diseases)}")
                content = await self.scrape_disease_content(page, disease)
                if content:
                    self.scraped_data.append(content)
                await asyncio.sleep(1)  # Be polite to the server
            
            await browser.close()
        
        print(f"\nSuccessfully scraped {len(self.scraped_data)} diseases")
    
    def save_data(self, filename="mayo_clinic_playwright_data.json"):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        print(f"Saved data to {filename}")
    
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
                    "type": "mayo_clinic_playwright_scraped"
                }
            )
            documents.append(doc)
        
        # Split into chunks
        chunked_docs = self.data_loader.text_splitter.split_documents(documents)
        print(f"Created {len(chunked_docs)} document chunks from {len(self.scraped_data)} diseases")
        return chunked_docs

async def main():
    print("Starting Mayo Clinic scraping with Playwright...")
    
    scraper = MayoClinicPlaywrightScraper()
    
    # Scrape all diseases
    await scraper.scrape_all_diseases()
    
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
    
    print("\nScraping and setup complete!")
    print(f"Total diseases processed: {len(scraper.scraped_data)}")
    print("You can now use the RAG system to answer health questions.")

if __name__ == "__main__":
    asyncio.run(main()) 