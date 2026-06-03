from flask import Flask, render_template, request, jsonify
from playwright.sync_api import sync_playwright
import time
from urllib.parse import urlparse

app = Flask(__name__)

def clean_url(url):
    """Clean and validate URL"""
    if not url:
        return None
    
    # Remove DuckDuckGo redirect if present
    if '//duckduckgo.com/l/' in url:
        # Extract the actual URL from DuckDuckGo redirect
        import re
        match = re.search(r'uddg=([^&]+)', url)
        if match:
            from urllib.parse import unquote
            return unquote(match.group(1))
    
    # Ensure URL has protocol
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/'):
        return None  # Skip relative links
    elif not url.startswith('http'):
        url = 'https://' + url
    
    return url

def classify_site(link, title):
    link = link.lower() if link else ""
    title = title.lower() if title else ""
    
    # Define keywords for each social site
    social_sites = {
        "Facebook": ["facebook.com", "facebook", "fb.com"],
        "Youtube": ["youtube.com", "youtube", "youtu.be"],
        "Telegram": ["telegram.org", "telegram", "t.me"],
        "Twitter": ["twitter.com", "x.com"],
        "Instagram": ["instagram.com"],
        "LinkedIn": ["linkedin.com"],
        "GitHub": ["github.com"],
        "Reddit": ["reddit.com"],
        "Wikipedia": ["wikipedia.org"]
    }
    for site, keywords in social_sites.items():
        if any(keyword in link for keyword in keywords):
            return site 
    
    # educational sites
    educational_sites = {
        "Coursera": ["coursera.org", "coursera"],
        "Udemy": ["udemy.com", "udemy"]
    }
    for site, keywords in educational_sites.items():
        if any(keyword in link for keyword in keywords):
            return site
    
    # news sites
    news_sites = ["cnn.com", "bbc.com", "aljazeera.com", "reuters.com", "apnews.com"]   
    if any(keyword in link for keyword in news_sites):
        return "News Site" 
    
    # email 
    if any(keyword in title for keyword in ["mailto:", "email", "mail", "@"]):
        return "Email Address"
    
    # phone number
    if any(keyword in title for keyword in ["tel:", "phone", "call", "+"]):
        return "Phone Number"
    
    # Government sites
    government_sites = [".gov", "gouv", "gob", "state.gov"]
    if any(keyword in link for keyword in government_sites):
        return "Government Site"
    
    general_sites = ["github.com", "archive.org", "wikipedia.org"]
    if any(keyword in link for keyword in general_sites):
        return "General Site"
    return "Website"

def osint_ex(query):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            # Navigate to DuckDuckGo
            page.goto(f"https://duckduckgo.com/?q={query}&t=h_&ia=web", timeout=60000, wait_until="networkidle")
            
            # Wait for results
            time.sleep(3)
            
            # Try multiple selectors
            selectors = ['[data-testid="result"]', '.result', 'article[data-testid="result"]', 'li.result']
            results_found = False
            
            for selector in selectors:
                try:
                    page.wait_for_selector(selector, timeout=10000)
                    results_found = True
                    print(f"Found results with selector: {selector}")
                    break
                except:
                    continue
            
            if not results_found:
                print("No results selector found")
                browser.close()
                return []
            
            all_results = []
            seen_links = set()
            
            # Get all results
            results = []
            for selector in selectors:
                results = page.query_selector_all(selector)
                if results:
                    break
            
            print(f"Found {len(results)} results")
            
            for result in results:
                try:
                    # Get title and link
                    title_elem = None
                    link_elem = None
                    
                    # Try different selectors for title
                    title_selectors = ['[data-testid="result-title-a"]', 'h2 a', 'h2', '.result__a', 'a.result__a']
                    for ts in title_selectors:
                        title_elem = result.query_selector(ts)
                        if title_elem:
                            break
                    
                    # Get link element
                    link_selectors = ['a[href]', '[data-testid="result-title-a"]', 'a.result__a']
                    for ls in link_selectors:
                        link_elem = result.query_selector(ls)
                        if link_elem:
                            break
                    
                    if title_elem and link_elem:
                        title_text = title_elem.inner_text().strip()
                        raw_link = link_elem.get_attribute('href')
                        
                        # Clean the URL
                        clean_link = clean_url(raw_link)
                        
                        # Get image
                        img_elem = result.query_selector('img')
                        img_src = img_elem.get_attribute('src') if img_elem else None
                        
                        # Validate and add result
                        if title_text and clean_link and 'duckduckgo.com' not in clean_link and clean_link not in seen_links:
                            # Check if it's a valid URL
                            if clean_link.startswith('http'):
                                seen_links.add(clean_link)
                                site_type = classify_site(clean_link, title_text)
                                all_results.append({
                                    "title": title_text,
                                    "link": clean_link,
                                    "image": img_src,
                                    "type": site_type
                                })
                                print(f"Added: {title_text[:50]} -> {clean_link[:80]}")
                                
                except Exception as e:
                    print(f"Error processing result: {e}")
                    continue
            
            browser.close()
            print(f"Total valid URLs extracted: {len(all_results)}")
            return all_results
            
    except Exception as e:
        print(f"Error in osint_ex: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify([]), 400
    
    results = osint_ex(query)
    print(f"Returning {len(results)} results for '{query}'")
    return jsonify(results)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🕵️ OSINT ANALYZER ULTIMATE")
    print("="*60)
    print(f"📍 Server: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)