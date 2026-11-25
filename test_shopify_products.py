import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

shop = os.getenv("SHOPIFY_STORE_DOMAIN")
client_id = os.getenv("SHOPIFY_CLIENT_ID")
client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")

# ---------------------------------------------------------
# 1. Get a Shopify access token
# ---------------------------------------------------------

token_url = f"https://{shop}/admin/oauth/access_token"

token_response = requests.post(
    token_url,
    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    },
    timeout=30,
)

token_response.raise_for_status()

access_token = token_response.json()["access_token"]

print("Authentication successful!")

# ---------------------------------------------------------
# 2. Query Shopify products
# ---------------------------------------------------------

graphql_url = f"https://{shop}/admin/api/2026-07/graphql.json"

query = """
query GetProducts {
  products(first: 5) {
    nodes {
      id
      title
      handle
      vendor
      productType
      status
      tags
    }
  }
}
"""

response = requests.post(
    graphql_url,
    headers={
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token,
    },
    json={
        "query": query
    },
    timeout=30,
)

print("Product API HTTP Status:", response.status_code)

response.raise_for_status()

result = response.json()

# GraphQL can return HTTP 200 while still containing GraphQL errors.
if result.get("errors"):
    print("GraphQL errors:")
    print(result["errors"])
    raise SystemExit(1)

products = result["data"]["products"]["nodes"]

print(f"Products returned: {len(products)}")
print()

for number, product in enumerate(products, start=1):
    print(f"PRODUCT {number}")
    print("ID:", product["id"])
    print("Title:", product["title"])
    print("Handle:", product["handle"])
    print("Vendor:", product["vendor"])
    print("Product Type:", product["productType"])
    print("Status:", product["status"])
    print("Tags:", product["tags"])
    print("-" * 60)