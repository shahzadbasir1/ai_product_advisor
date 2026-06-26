import json

from models.product import Product


def load_products_json(
    file_path: str,
    catalog_id: str
) -> list[Product]:

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = []

    for item in data:

        item["source_catalog_id"] = catalog_id

        product = Product(**item)

        products.append(product)

    return products