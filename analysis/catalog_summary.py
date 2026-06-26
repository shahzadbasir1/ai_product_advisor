from models.product import Product


def generate_catalog_summary(
    products: list[Product]
):

    vendors = set()

    categories = set()

    product_types = set()

    inventory_total = 0

    prices = []

    for product in products:

        vendors.add(product.vendor)

        categories.add(product.category)

        if product.product_type:
            product_types.add(
                product.product_type
            )

        if product.inventory_qty:

            inventory_total += (
                product.inventory_qty
            )

        prices.append(product.price)

    return {

        "total_products":
            len(products),

        "vendors":
            len(vendors),

        "categories":
            len(categories),

        "product_types":
            len(product_types),

        "inventory_total":
            inventory_total,

        "min_price":
            min(prices)
            if prices else 0,

        "max_price":
            max(prices)
            if prices else 0
    }