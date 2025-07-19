import asyncio
import json
import time
from agentql import AgentQL
from data_loader import MedicalDataLoader
from rag_system import HealthRAGSystem
from langchain.schema import Document

class MayoClinicAgentQLScraper:
    def __init__(self):
        self.agentql = AgentQL()
        self.data_loader = MedicalDataLoader()
        self.scraped_data = []
        
    async def scrape_letter_page(self, letter):
        """Scrape a single letter page to get all disease URLs"""
        print(f"Scraping letter {letter}...")
        
        query = f"""
        query {{
            page(url: "https://www.mayoclinic.org/diseases-conditions/index?letter={letter}") {{
                diseases: elements(selector: "a[href*='/diseases-conditions/'][href*='/symptoms-causes/']") {{
                    name: text
                    url: attr("href")
                }}
            }}
        }}
        """
        
        try:
            result = await self.agentql.run(query)
            if result and 'page' in result and 'diseases' in result['page']:
                diseases = result['page']['diseases']
                print(f"  Found {len(diseases)} diseases for letter {letter}")
                return diseases
            else:
                print(f"  No diseases found for letter {letter}")
                return []
        except Exception as e:
            print(f"  Error scraping letter {letter}: {e}")
            return []
    
    async def scrape_disease_content(self, disease_info):
        """Scrape content from a specific disease page"""
        url = disease_info['url']
        if not url.startswith('http'):
            url = f"https://www.mayoclinic.org{url}"
            
        print(f"Scraping disease content: {disease_info['name']}")
        
        query = f"""
        query {{
            page(url: "{url}") {{
                title: element(selector: "h1") {{
                    text: text
                }}
                content: element(selector: "div.content, main, article") {{
                    text: text
                }}
                symptoms: elements(selector: "h2, h3") {{
                    text: text
                }}
            }}
        }}
        """
        
        try:
            result = await self.agentql.run(query)
            if result and 'page' in result:
                page_data = result['page']
                
                # Extract title
                title = "Unknown"
                if 'title' in page_data and page_data['title']:
                    title = page_data['title'].get('text', 'Unknown')
                
                # Extract content
                content = ""
                if 'content' in page_data and page_data['content']:
                    content = page_data['content'].get('text', '')
                
                # Extract symptoms and other sections
                sections = []
                if 'symptoms' in page_data and page_data['symptoms']:
                    sections = [s.get('text', '') for s in page_data['symptoms']]
                
                # Combine all content
                full_content = f"{content}\n\n" + "\n".join(sections)
                
                if len(full_content.strip()) > 100:  # Only save if we have substantial content
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
                print(f"  No content found for {disease_info['name']}")
                return None
                
        except Exception as e:
            print(f"  Error scraping {disease_info['name']}: {e}")
            return None
    
    async def scrape_all_diseases(self):
        """Scrape all diseases from A-Z"""
        import string
        
        all_diseases = []
        
        # Scrape all letter pages to get disease URLs
        for letter in string.ascii_uppercase:
            diseases = await self.scrape_letter_page(letter)
            all_diseases.extend(diseases)
            await asyncio.sleep(1)  # Be polite to the server
        
        print(f"\nFound {len(all_diseases)} total diseases to scrape")
        
        # Scrape content from each disease page
        for i, disease in enumerate(all_diseases, 1):
            print(f"\nProgress: {i}/{len(all_diseases)}")
            content = await self.scrape_disease_content(disease)
            if content:
                self.scraped_data.append(content)
            await asyncio.sleep(1)  # Be polite to the server
        
        print(f"\nSuccessfully scraped {len(self.scraped_data)} diseases")
    
    def save_data(self, filename="mayo_clinic_agentql_data.json"):
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
                    "type": "mayo_clinic_agentql_scraped"
                }
            )
            documents.append(doc)
        
        # Split into chunks
        chunked_docs = self.data_loader.text_splitter.split_documents(documents)
        print(f"Created {len(chunked_docs)} document chunks from {len(self.scraped_data)} diseases")
        return chunked_docs

async def main():
    print("Starting Mayo Clinic scraping with AgentQL...")
    
    scraper = MayoClinicAgentQLScraper()
    
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