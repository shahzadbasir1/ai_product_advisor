from api_client import load_shopify_products_api


products = load_shopify_products_api(limit=5)

print("Products returned:", len(products))
print()

for product in products:
    print("Title:", product["title"])
    print("Price:", product["price"])
    print("Status:", product["status"])
    print("Source:", product["source_catalog_id"])
    print("-" * 60)