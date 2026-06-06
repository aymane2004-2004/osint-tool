from flask import Flask, render_template, request, jsonify
from playwright.sync_api import sync_playwright
import time
import re
from urllib.parse import urlparse, unquote

app = Flask(__name__)

def clean_url(url):
    """Clean and validate URL — unwraps ALL DuckDuckGo redirect formats."""
    if not url:
        return None

    # Normalise protocol-relative before checking
    if url.startswith('//'):
        url = 'https:' + url

    # ── Unwrap DDG redirect (https:// AND // forms) ──────────────────────────
    # DDG puts every href through: https://duckduckgo.com/l/?uddg=<encoded>&rut=…
    if 'duckduckgo.com/l/' in url:
        match = re.search(r'[?&]uddg=([^&]+)', url)
        if match:
            return clean_url(unquote(match.group(1)))   # recurse once for safety
        return None   # DDG internal link we can't unwrap → discard

    # Drop any remaining duckduckgo.com URLs (settings, feedback, etc.)
    if 'duckduckgo.com' in url:
        return None

    # Relative paths → discard
    if url.startswith('/'):
        return None

    # Add scheme if missing
    if not url.startswith('http'):
        url = 'https://' + url

    return url


def classify_site(link, title):
    link = link.lower() if link else ""
    title = title.lower() if title else ""
    
    social_sites = {
        "Facebook":  ["facebook.com", "fb.com"],
        "Youtube":   ["youtube.com", "youtu.be"],
        "Telegram":  ["telegram.org", "t.me"],
        "Twitter":   ["twitter.com", "x.com"],
        "Instagram": ["instagram.com"],
        "LinkedIn":  ["linkedin.com"],
        "GitHub":    ["github.com"],
        "Reddit":    ["reddit.com"],
        "Wikipedia": ["wikipedia.org"],
        "TikTok":    ["tiktok.com"],
    }
    for site, keywords in social_sites.items():
        if any(k in link for k in keywords):
            return site

    educational_sites = {
        "Coursera": ["coursera.org"],
        "Udemy":    ["udemy.com"],
        "Medium":   ["medium.com"],
    }
    for site, keywords in educational_sites.items():
        if any(k in link for k in keywords):
            return site

    news_sites = ["cnn.com", "bbc.com", "aljazeera.com", "reuters.com",
                  "apnews.com", "theguardian.com", "nytimes.com", "bloomberg.com"]
    if any(k in link for k in news_sites):
        return "News Site"

    if any(k in title for k in ["mailto:", "@"]):
        return "Email Address"
    if any(k in title for k in ["tel:", "phone"]):
        return "Phone Number"

    government_sites = [".gov", "gouv", ".gob.", "state.gov"]
    if any(k in link for k in government_sites):
        return "Government Site"

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

            # ── Speed: block images / fonts / stylesheets ────────────────────
            def block_assets(route):
                if route.request.resource_type in ('image', 'stylesheet', 'font', 'media'):
                    route.abort()
                else:
                    route.continue_()
            page.route("**/*", block_assets)

            # ── Navigate ─────────────────────────────────────────────────────
            page.goto(
                f"https://duckduckgo.com/?q={query}&t=h_&ia=web",
                timeout=60000,
                wait_until="domcontentloaded"   # FIXED: was "networkidle" (hangs)
            )

            # ── Wait for result containers ───────────────────────────────────
            selectors = [
                'article[data-testid="result"]',
                '[data-testid="result"]',
                'li.result',
                '.result',
            ]
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

            # ── Collect result elements ──────────────────────────────────────
            results = []
            for selector in selectors:
                results = page.query_selector_all(selector)
                if results:
                    break

            print(f"Found {len(results)} result containers")

            all_results = []
            seen_links = set()

            # Selectors for the title <a> element inside each result
            # These are also the link elements — get href from the same element!
            title_selectors = [
                '[data-testid="result-title-a"]',   # modern DDG
                'h2 a',                              # fallback
                '.result__a',                        # old DDG
                'a.result__a',
            ]

            for result in results:
                try:
                    # ── BUG FIX: find the title <a> element ─────────────────
                    # Then get BOTH text and href from the SAME element.
                    # The old code used a separate link_selectors list starting
                    # with 'a[href]' which matched the favicon anchor first,
                    # giving a wrong/internal URL while the title was correct.
                    title_elem = None
                    for ts in title_selectors:
                        title_elem = result.query_selector(ts)
                        if title_elem:
                            break

                    if not title_elem:
                        continue

                    title_text = title_elem.inner_text().strip()

                    # ── href comes from the SAME element as the title ────────
                    raw_link = title_elem.get_attribute('href')
                    clean_link = clean_url(raw_link)

                    if (title_text and clean_link
                            and clean_link.startswith('http')
                            and clean_link not in seen_links):

                        seen_links.add(clean_link)
                        site_type = classify_site(clean_link, title_text)

                        # Optional snippet
                        snip_el = result.query_selector('[data-testid="result-snippet"]') \
                                  or result.query_selector('.result__snippet')
                        snippet = snip_el.inner_text().strip() if snip_el else ""

                        all_results.append({
                            "title":   title_text,
                            "link":    clean_link,
                            "snippet": snippet,
                            "image":   None,
                            "type":    site_type,
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