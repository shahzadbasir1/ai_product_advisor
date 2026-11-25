from ingestion.shopify_loader import (
    load_shopify_products
)


products = load_shopify_products(limit=10)

print("Products loaded:", len(products))
print()

for product in products:
    print("Title:", product.title)
    print("Product ID:", product.product_id)
    print("Description:", product.description)
    print("Vendor:", product.vendor)
    print("Category:", product.category)
    print("Price:", product.price)
    print("Status:", product.status)
    print("Product Type:", product.product_type)
    print("Tags:", product.tags)
    print("Inventory:", product.inventory_qty)
    print("Image:", product.image_url)
    print("Variants:", len(product.variants))
    print(
        "Source Catalog:",
        product.source_catalog_id
    )
    print("-" * 70)