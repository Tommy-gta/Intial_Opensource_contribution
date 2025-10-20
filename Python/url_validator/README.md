# URL Validator with Safety Check

A Python script to validate URLs, check their reachability, and verify their safety using Google Safe Browsing API.


## Introduction

This script helps to validate URLs by:
1. Checking if the URL is syntactically correct.
2. Verifying if the URL is reachable (e.g., not 404 or 500).
3. Checking if the URL is marked as unsafe by Google Safe Browsing.


## Features

- URL Syntax Validation: Ensures the URL is properly formatted.
- Reachability Check: Confirms if the URL is accessible and returns a valid HTTP status code.
- Safety Check: Uses Google Safe Browsing API to detect malicious or unsafe sites.
- User-Agent Header: Mimics a browser to avoid being blocked by servers.
- Error Handling: Gracefully handles connection errors, timeouts, and API issues.
- Automatic HTTPS: Adds `https://` if the user forgets it.

---

## Usage

### Prerequisites

- Python 3.x
- Required libraries: `validators`, `requests`, and `google-api-python-client`.

#### Google Safe Browsing API Key
1. Get an API key from [Google Cloud Console](https://console.cloud.google.com/apis/library/safebrowsing.googleapis.com).
2. Replace `GOOGLE_SAFE_BROWSING_API_KEY` in the script with your actual API key.

### Install the dependencies:
```bash
pip install validators requests google-api-python-client
```

### Running the Script

- Save the script as url_validator.py.
- Run the script:
```bash
python url_validator.py
```
- Enter the URL you want to validate when prompted.

#### Example Outputs
 
##### Valid and Safe URL 
  
```json
{
  "valid": true,
  "url": "https://www.example.com",
  "message": "URL is valid, reachable, and safe."
}
```
 
##### Invalid URL 

```json
{
  "valid": false,
  "url": "example",
  "error": "Invalid URL format."
}
``` 
 
##### Unreachable URL 

```json
{
  "valid": false,
  "url": "https://nonexistent-site.com",
  "error": "URL is unreachable (e.g., 404, DNS error, or server down)."
}
``` 
 
##### Unsafe URL 
 
```json
{
  "valid": false,
  "url": "https://malicious-site.com",
  "error": "Warning: This URL is marked as UNSAFE by Google Safe Browsing!"
}
```

### License
This project is licensed under the MIT License.
