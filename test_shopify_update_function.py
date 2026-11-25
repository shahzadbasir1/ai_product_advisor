from ingestion.shopify_loader import update_shopify_product


PRODUCT_ID = "gid://shopify/Product/15586470592680"

NEW_DESCRIPTION = (
    "Description updated through the reusable AI Product Advisor "
    "Shopify integration function."
)


print("Updating Shopify product...")
print()

product = update_shopify_product(
    product_id=PRODUCT_ID,
    description=(
        "AI-enhanced product description created by "
        "AI Product Advisor."
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
print("Title:", product.title)
print("Product ID:", product.product_id)
print("Description:", product.description)
print("Product Type:", product.product_type)
print("Tags:", product.tags)
print("Status:", product.status)
print("Price:", product.price)
print("Inventory:", product.inventory_qty)
print("Source:", product.source_catalog_id)