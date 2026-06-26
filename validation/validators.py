from urllib.parse import urlparse

from models.product import Product


VALID_STATUSES = [
    "active",
    "draft",
    "archived"
]


def validate_product(product: Product):

    errors = []

    if not product.product_id:
        errors.append("product_id is required")

    if not product.title:
        errors.append("title is required")

    if not product.description:
        errors.append("description is required")

    if not product.vendor:
        errors.append("vendor is required")

    if not product.category:
        errors.append("category is required")

    if product.price < 0:
        errors.append("price must be >= 0")

    if product.status.lower() not in VALID_STATUSES:
        errors.append("invalid status")

    if (
        product.inventory_qty is not None
        and product.inventory_qty < 0
    ):
        errors.append(
            "inventory_qty must be >= 0"
        )

    if product.product_url:

        parsed = urlparse(product.product_url)

        if parsed.scheme not in [
            "http",
            "https"
        ]:

            errors.append(
                "product_url must start with http:// or https://"
            )

    return errors