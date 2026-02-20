import json

try:
    from safaribooks import COOKIES_FILE
except ImportError:
    COOKIES_FILE = "cookies.json"

try:
    import browser_cookie3
except ImportError:
    raise ImportError("Please run this program via: uv run --with browser_cookie3 python retrieve_cookies.py")

def get_oreilly_cookies():
    cookies = {}
    
    # Explicitly call browsers to avoid the Arc/NoneType bug on Linux
    browsers = [
        browser_cookie3.firefox,
        browser_cookie3.chrome,
        browser_cookie3.chromium,
        browser_cookie3.brave,
        browser_cookie3.opera,
        browser_cookie3.edge
    ]
    
    for browser_fn in browsers:
        try:
            cj = browser_fn(domain_name='oreilly.com')
            for c in cj:
                cookies[c.name] = c.value
        except Exception:
            # Skip browsers that aren't installed or have locked databases
            continue

    return cookies

def main():
    cookies = get_oreilly_cookies()
    if not cookies:
        print("Could not find any oreilly.com cookies. Ensure you are logged into O'Reilly via a supported browser.")
        return
        
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)
    print(f"Cookies saved to {COOKIES_FILE}")

if __name__ == "__main__":
    main()
