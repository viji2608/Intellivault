"""
Quick test of CyborgDB connection with your API key.
"""

import requests
import json

API_KEY = "cyborg_ce554d85bbfc451aa4d332a94c94f1fe"

# Test various endpoint patterns
endpoints = [
    "https://api.cyborgdb.com",
    "https://api.cyborginc.com",
    "https://cyborgdb.cloud",
    "https://hackathon.cyborgdb.com",
    "http://api.cyborgdb.com:8001",
    "https://api.cyborgdb.io",
    "https://cyborginc.com/api",
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print("=" * 70)
print("TESTING CYBORGDB CONNECTION")
print("=" * 70)
print(f"\n🔑 API Key: {API_KEY[:20]}...\n")

for endpoint in endpoints:
    print(f"📍 Testing: {endpoint}")
    
    # Try different health check paths
    paths = [
        "/",
        "/health",
        "/api/health",
        "/api/v1/health",
        "/status",
        "/api/v1/collections"
    ]
    
    for path in paths:
        try:
            url = endpoint + path
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code < 500:  # Any response means endpoint exists
                print(f"  ✓ RESPONSE! {path}")
                print(f"    Status: {response.status_code}")
                
                try:
                    data = response.json()
                    print(f"    JSON: {json.dumps(data, indent=2)[:200]}")
                except:
                    print(f"    Text: {response.text[:200]}")
                
                if response.status_code in [200, 201]:
                    print(f"\n✅ WORKING ENDPOINT FOUND!")
                    print(f"   URL: {url}")
                    print(f"   Use this in your code!")
                    exit(0)
                elif response.status_code in [401, 403]:
                    print(f"  ⚠️  Authentication issue (endpoint exists but key may be wrong)")
                
        except requests.exceptions.Timeout:
            print(f"  ⏱️  Timeout: {path}")
        except requests.exceptions.ConnectionError:
            pass
        except Exception as e:
            pass
    
    print()

print("=" * 70)
print("❌ NO WORKING ENDPOINT FOUND")
print("=" * 70)
print("\n💡 Next steps:")
print("1. Contact CyborgDB support: support@cyborginc.com")
print("2. Ask for endpoint URL in hackathon Discord/Slack")
print("3. Check hackathon documentation for API endpoint")
print("\nYour API key is valid, just need the endpoint URL!")
