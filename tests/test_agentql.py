import asyncio
from agentql import async_api

async def test_agentql():
    print("Testing AgentQL with Mayo Clinic...")
    
    # Test with a simple query to get the page title
    query = """
    query {
        page(url: "https://www.mayoclinic.org/diseases-conditions/index?letter=A") {
            title: element(selector: "h1") {
                text: text
            }
            links: elements(selector: "a[href*='/diseases-conditions/']") {
                text: text
                url: attr("href")
            }
        }
    }
    """
    
    try:
        print("Running AgentQL query...")
        result = await async_api.run(query)
        
        if result and 'page' in result:
            page_data = result['page']
            
            # Print title
            if 'title' in page_data and page_data['title']:
                print(f"Page title: {page_data['title'].get('text', 'Unknown')}")
            
            # Print some links
            if 'links' in page_data and page_data['links']:
                links = page_data['links']
                print(f"Found {len(links)} disease links")
                
                # Show first 5 links
                for i, link in enumerate(links[:5]):
                    print(f"  {i+1}. {link.get('text', 'Unknown')} -> {link.get('url', 'Unknown')}")
            else:
                print("No links found")
        else:
            print("No result returned")
            
    except Exception as e:
        print(f"Error testing AgentQL: {e}")

if __name__ == "__main__":
    asyncio.run(test_agentql()) 