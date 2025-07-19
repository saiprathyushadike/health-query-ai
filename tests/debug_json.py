import requests
import re
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def test_json_extraction():
    url = "https://www.mayoclinic.org/diseases-conditions/index?letter=A"
    resp = requests.get(url, headers=HEADERS)
    
    print("Testing JSON extraction...")
    
    # Look for the results object within searchresults
    pattern = r'"results":\s*\{[^}]*"items":\s*\[(.*?)\][^}]*\}'
    match = re.search(pattern, resp.text, re.DOTALL)
    
    if match:
        print(f"Found results match!")
        items_text = match.group(1)
        print(f"Length: {len(items_text)}")
        print(f"First 500 chars: {items_text[:500]}")
        
        try:
            # Try to parse the items array
            items_json = "[" + items_text + "]"
            items_data = json.loads(items_json)
            print(f"Successfully parsed items JSON with {len(items_data)} letter groups")
            
            url_count = 0
            for letter_group in items_data:
                if "items" in letter_group:
                    for disease in letter_group["items"]:
                        if "url" in disease and "/symptoms-causes/" in disease["url"]:
                            url_count += 1
                            print(f"  Found URL: {disease['url']}")
            
            print(f"Total symptoms-causes URLs: {url_count}")
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse items JSON: {e}")
            print(f"JSON text: {items_text[:300]}...")
            
            # Try to find where the JSON is malformed
            print("\nTrying to find the complete structure...")
            # Look for the complete results object with proper boundaries
            full_pattern = r'"results":\s*\{.*?"items":\s*\[.*?\].*?\}'
            full_match = re.search(full_pattern, resp.text, re.DOTALL)
            if full_match:
                print(f"Found full results object! Length: {len(full_match.group(0))}")
                print(f"First 300 chars: {full_match.group(0)[:300]}")
            else:
                print("No full results object found")
    else:
        print("No results match found")

if __name__ == "__main__":
    test_json_extraction() 