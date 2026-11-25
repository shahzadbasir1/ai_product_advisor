import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

SHOP = os.getenv("SHOPIFY_STORE_DOMAIN")
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")

API_VERSION = "2026-07"

PRODUCT_ID = "gid://shopify/Product/15586470592680"
####gid://shopify/Product/15586470559912

# ---------------------------------------------------------
# 1. Get Shopify access token
# ---------------------------------------------------------

token_response = requests.post(
    f"https://{SHOP}/admin/oauth/access_token",
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    },
    timeout=30,
)

token_response.raise_for_status()

access_token = token_response.json()["access_token"]

print("Authentication successful!")


# ---------------------------------------------------------
# 2. Update ONE field: description
# ---------------------------------------------------------

graphql_url = (
    f"https://{SHOP}/admin/api/"
    f"{API_VERSION}/graphql.json"
)

mutation = """
mutation UpdateProduct($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      title
      description
      status
    }
    userErrors {
      field
      message
    }
  }
}
"""

new_description = (
    "Test description written by AI Product Advisor "
    "during Shopify write integration testing."
)

response = requests.post(
    graphql_url,
    headers={
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token,
    },
    json={
        "query": mutation,
        "variables": {
            "product": {
                "id": PRODUCT_ID,
                "descriptionHtml": new_description,
            }
        },
    },
    timeout=30,
)

print("Update HTTP Status:", response.status_code)

response.raise_for_status()

result = response.json()

if result.get("errors"):
    print("GraphQL errors:")
    print(result["errors"])
    raise SystemExit(1)

update_result = result["data"]["productUpdate"]

if update_result["userErrors"]:
    print("Shopify user errors:")
    for error in update_result["userErrors"]:
        print(
            error["field"],
            "-",
            error["message"]
        )
    raise SystemExit(1)

product = update_result["product"]

print()
print("UPDATE SUCCESSFUL")
print("ID:", product["id"])
print("Title:", product["title"])
print("Status:", product["status"])
print("Description:", product["description"])