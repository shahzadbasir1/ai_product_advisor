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
            issues.append({
                "product_id": product.product_id,
                "severity": "Critical",
                "issue": "Missing URL"
            })

        if not product.description:
            summary["missing_description"] += 1
            issues.append(
                {
                    "product_id": product.product_id,
                    "severity": "Warning",
                    "issue": "Missing Description"
                }
            )

        if not product.vendor:
            summary["missing_vendor"] += 1
            issues.append(
                {
                    "product_id": product.product_id,
                    "severity": "Warning",
                    "issue": "Missing Vendor"
                }
            )

        if not product.category:
            summary["missing_category"] += 1
            issues.append(
                {
                    "product_id": product.product_id,
                    "severity": "Warning",
                    "issue": "Missing Category"
                }
            )

        if not product.image_url:
            summary["missing_image"] += 1
            issues.append(
                {
                    "product_id": product.product_id,
                    "severity": "Critical",
                    "issue": "Missing Image"
                }
            )

        if len(product.tags) == 0:
            summary["missing_tags"] += 1
            issues.append(
                {
                    "product_id": product.product_id,
                    "severity": "Warning",
                    "issue": "Missing Tags"
                }
            )

        if not product.product_type:
            summary["missing_product_type"] += 1
            issues.append(
                {
                    "product_id": product.product_id,
                    "severity": "Critical",
                    "issue": "Missing Product Type"
                }
            )

        if product.inventory_qty is None:
            summary["missing_inventory"] += 1
            issues.append(
                {
                    "product_id": product.product_id,
                    "severity": "Warning",
                    "issue": "Missing Inventory"
                }
            )

        severity_order = {
            "Critical": 0,
            "Warning": 1
        }

        issues.sort(
            key=lambda issue: (
                severity_order[issue["severity"]],
                issue["product_id"]
            )
        )

    return summary, issues