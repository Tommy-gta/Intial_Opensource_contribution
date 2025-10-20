import validators
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

# --- Google Safe Browsing API Setup ---
# REPLACE with your own API key from: https://console.cloud.google.com/apis/library/safebrowsing.googleapis.com
SAFE_BROWSING_API_KEY = "GOOGLE_SAFE_BROWSING_API_KEY"

# Define a common browser User-Agent to avoid being blocked
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def is_valid_url(url):
    """Check if the URL is syntactically valid."""
    return validators.url(url)

def is_url_reachable(url, timeout=5):
    """Check if the URL is reachable (responds to a request)."""
    try:
        # Use HEAD to be efficient (don't download body)
        # Add User-Agent and allow redirects
        response = requests.head(url, 
                                 timeout=timeout, 
                                 allow_redirects=True, 
                                 headers=HTTP_HEADERS)
        
        # response.ok checks for status codes < 400 (e.g., 200, 301, 302)
        # This is a better check for "reachability" than just '== 200'
        print(f"Debug: Status code for {url}: {response.status_code}", file=sys.stderr)
        return response.ok
    except requests.RequestException:
        # Catches DNS errors, timeouts, connection errors, etc.
        return False

def check_url_safety(url):
    """
    Check if the URL is marked as unsafe by Google Safe Browsing.
    Returns:
        - True: If the URL is confirmed safe (no matches).
        - False: If the URL is confirmed unsafe (matches found).
        - None: If the API check failed (e.g., bad API key, network error).
    """
    if SAFE_BROWSING_API_KEY == "GOOGLE_SAFE_BROWSING_API_KEY":
        print("Error: SAFE_BROWSING_API_KEY is not set. Skipping safety check.", file=sys.stderr)
        return None # Indicate the check failed

    try:
        service = build("safebrowsing", "v4", developerKey=SAFE_BROWSING_API_KEY)
        
        payload = {
            "client": {
                "clientId": "my-validation-script", # Change this to your app name
                "clientVersion": "1.0.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        
        response = service.threatMatches().find(body=payload).execute()
        
        # If 'matches' key exists and is not empty, it's unsafe
        if response.get("matches"):
            return False
        else:
            return True # No matches found, URL is safe
            
    except HttpError as e:
        # Handle API-specific errors (e.g., bad API key, quota exceeded)
        print(f"Error: Google Safe Browsing API call failed: {e}", file=sys.stderr)
        return None
    except Exception as e:
        # Handle other errors (e.g., no internet connection)
        print(f"Error: An unexpected error occurred during safety check: {e}", file=sys.stderr)
        return None

def validate_url(url):
    """Validate URL, check reachability, and safety."""
    
    # 1. Check syntax
    if not is_valid_url(url):
        return {"valid": False, "url": url, "error": "Invalid URL format."}

    # 2. Check reachability
    if not is_url_reachable(url):
        return {"valid": False, "url": url, "error": "URL is unreachable (e.g., 404, DNS error, or server down)."}

    # 3. Check safety
    is_safe = check_url_safety(url)
    
    if is_safe is False: # Explicitly check for False
        return {"valid": False, "url": url, "error": "Warning: This URL is marked as UNSAFE by Google Safe Browsing!"}
    
    if is_safe is None: # Explicitly check for None
        return {
            "valid": True, 
            "url": url,
            "message": "URL is valid and reachable.",
            "warning": "Could not perform safety check (API error or key issue)."
        }

    # If we get here, is_safe must be True
    return {"valid": True, "url": url, "message": "URL is valid, reachable, and safe."}

# --- Example Usage ---
if __name__ == "__main__":
    try:
        url_to_test = input("Enter URL to validate: ")
        
        # Simple fix in case user forgets 'http://'
        if not url_to_test.startswith(('http://', 'https://')):
            print(f"Assuming 'https://'. Testing: https://{url_to_test}")
            url_to_test = 'https://' + url_to_test
            
        result = validate_url(url_to_test)
        print("\n--- Validation Result ---")
        print(result)
        
    except KeyboardInterrupt:
        print("\nValidation cancelled.")
