import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

shop = os.getenv("SHOPIFY_STORE_DOMAIN")
client_id = os.getenv("SHOPIFY_CLIENT_ID")
client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")

print("Shop:", shop)
print("Client ID loaded:", bool(client_id))
print("Client Secret loaded:", bool(client_secret))

url = f"https://{shop}/admin/oauth/access_token"

response = requests.post(
    url,
    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    },
    timeout=30,
)

print("HTTP Status:", response.status_code)

if response.ok:
    data = response.json()

    print("Authentication successful!")
    print("Access token received:", bool(data.get("access_token")))
    print("Scopes:", data.get("scope"))
    print("Expires in:", data.get("expires_in"), "seconds")
else:
    print("Authentication failed.")
    print(response.text)