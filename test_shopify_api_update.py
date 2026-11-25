from api_client import update_shopify_product_api


PRODUCT_ID = "gid://shopify/Product/15586470592680"


print("Updating Shopify product through FastAPI...")
print()

product = update_shopify_product_api(
    product_id=PRODUCT_ID,
    description=(
        "Product description updated through the "
        "AI Product Advisor FastAPI service."
    ),
    product_type="Premium Snowboard",
    tags=[
        "Snowboard",
        "Winter",
        "Sport",
        "Premium",
    ],
)

print("UPDATE SUCCESSFUL")
print("Title:", product["title"])
print("Product ID:", product["product_id"])
print("Description:", product["description"])
print("Product Type:", product["product_type"])
print("Tags:", product["tags"])
print("Status:", product["status"])
print("Price:", product["price"])
print("Inventory:", product["inventory_qty"])
print("Source:", product["source_catalog_id"])