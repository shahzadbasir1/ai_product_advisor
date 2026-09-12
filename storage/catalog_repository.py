from models.product import Product
import json
import os
from typing import List

def load_catalog(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    products = [
        Product(**item)
        for item in data
    ]

    return products

def save_catalog(products, file_path):

    print("=" * 80)
    print("Saving catalog...")
    print("File:", os.path.abspath(file_path))

    data = []

    for product in products:

        d = product.model_dump()

        print(d)

        data.append(d)

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            default=str
        )

    print("File written successfully.")

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        print("Contents of file after write:")
        print(f.read())

    print("=" * 80)

def save_uploaded_catalog(
    uploaded_file
):


    print("=" * 80)
    print("save_uploaded_catalog() called")
    print("Uploading:", uploaded_file.name)
    print("=" * 80)
    
    os.makedirs(
        "data/catalogs",
        exist_ok=True
    )

    catalog_path = (
        f"data/catalogs/{uploaded_file.name}"
    )

    with open(
        catalog_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getvalue()
        )

    return catalog_path

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