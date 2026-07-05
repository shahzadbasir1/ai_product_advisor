from typing import List

from models.product import Product


def merge_catalogs(
    existing_products: List[Product],
    uploaded_products: List[Product]
) -> List[Product]:
    """
    Merge two catalogs.

    Rules:
    - Existing products are preserved.
    - New products are added.
    - If the uploaded catalog contains an existing product_id,
      the uploaded version replaces the existing one.
    """

    merged = {
        product.product_id: product
        for product in existing_products
    }

    for product in uploaded_products:
        merged[product.product_id] = product

    return list(merged.values())