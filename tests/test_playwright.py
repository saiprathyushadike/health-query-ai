import asyncio
from playwright.async_api import async_playwright

async def test_playwright():
    print("Testing Playwright with Mayo Clinic...")
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set to False to see what's happening
        page = await browser.new_page()
        
        # Set user agent
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        try:
            # Navigate to Mayo Clinic index page
            url = "https://www.mayoclinic.org/diseases-conditions/index?letter=A"
            print(f"Navigating to {url}")
            
            # Use a shorter timeout and different wait strategy
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # Wait a bit for content to load
            await asyncio.sleep(3)
            
            # Extract page title
            title = await page.title()
            print(f"Page title: {title}")
            
            # Try to find any links first
            all_links = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('a');
                    return Array.from(links).map(link => ({
                        text: link.textContent.trim(),
                        href: link.href
                    })).filter(link => link.text.length > 0);
                }
            """)
            
            print(f"Found {len(all_links)} total links")
            
            # Show first 10 links to see what we're getting
            for i, link in enumerate(all_links[:10]):
                print(f"  {i+1}. {link['text']} -> {link['href']}")
            
            # Now try to find disease-specific links
            diseases = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('a[href*="/diseases-conditions/"][href*="/symptoms-causes/"]');
                    return Array.from(links).map(link => ({
                        name: link.textContent.trim(),
                        url: link.href
                    }));
                }
            """)
            
            print(f"\nFound {len(diseases)} disease links")
            
            # Show first 5 disease links
            for i, disease in enumerate(diseases[:5]):
                print(f"  {i+1}. {disease['name']} -> {disease['url']}")
            
        except Exception as e:
            print(f"Error testing Playwright: {e}")
        
        finally:
            # Keep browser open for a moment to see what happened
            await asyncio.sleep(5)
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_playwright()) 