from models.product import Product


def analyze_catalog_health(products: list[Product]):

    summary = {
        "missing_url": 0,
        "missing_description": 0,
        "missing_vendor": 0,
        "missing_category": 0,
        "missing_image": 0,
        "missing_tags": 0,
        "missing_product_type": 0,
        "missing_inventory": 0,
    }

    issues = []

    for product in products:

        if not product.product_url:
            summary["missing_url"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Product URL"
                }
            )

        if not product.description:
            summary["missing_description"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Description"
                }
            )

        if not product.vendor:
            summary["missing_vendor"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Vendor"
                }
            )

        if not product.category:
            summary["missing_category"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Category"
                }
            )

        if not product.image_url:
            summary["missing_image"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Image"
                }
            )

        if len(product.tags) == 0:
            summary["missing_tags"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Tags"
                }
            )

        if not product.product_type:
            summary["missing_product_type"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Product Type"
                }
            )

        if product.inventory_qty is None:
            summary["missing_inventory"] += 1
            issues.append(
                {
                    "Product ID": product.product_id,
                    "Issue": "Missing Inventory"
                }
            )

    return summary, issues