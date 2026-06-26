import pandas as pd

from models.product import Product


def load_shopify_csv(
    file_path: str,
    catalog_id: str
) -> list[Product]:

    df = pd.read_csv(file_path)

    products = []

    for _, row in df.iterrows():

        product = Product(
            product_id=str(row.get("Variant SKU", "")),
            title=str(row.get("Title", "")),
            description=str(row.get("Body (HTML)", "")),
            vendor=str(row.get("Vendor", "")),
            category=str(row.get("Product Category", "")),
            price=float(row.get("Variant Price", 0)),
            status=str(row.get("Status", "active")),

            handle=row.get("Handle"),

            product_type=row.get("Type"),

            inventory_qty=row.get("Variant Inventory Qty"),

            compare_at_price=row.get("Variant Compare At Price"),

            image_url=row.get("Image Src"),

            published=row.get("Published"),

            source_catalog_id=catalog_id
        )

        products.append(product)

    return products