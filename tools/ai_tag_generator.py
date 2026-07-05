from models.product import Product


def generate_tags(product: Product):

    tags = []

    ##################################################
    # Category
    ##################################################

    if product.category:
        tags.append(product.category)

    ##################################################
    # Product Type
    ##################################################

    if product.product_type:
        tags.append(product.product_type)

    ##################################################
    # Vendor
    ##################################################

    if product.vendor:
        tags.append(product.vendor)

    ##################################################
    # Title keywords
    ##################################################

    title = (product.title or "").lower()

    keyword_map = {

        "shampoo": "Shampoo",
        "conditioner": "Conditioner",
        "hair": "Hair Care",
        "moisture": "Moisturizing",
        "gold": "Premium",
        "repair": "Repair",
        "damage": "Damaged Hair",
        "dry": "Dry Hair",
        "frizz": "Anti-Frizz",
        "curl": "Curly Hair",
        "volume": "Volume",
        "color": "Color Protection"

    }

    for keyword, tag in keyword_map.items():

        if keyword in title:

            tags.append(tag)

    ##################################################
    # Description keywords
    ##################################################

    description = (
        product.description or ""
    ).lower()

    if "hydrate" in description:
        tags.append("Hydrating")

    if "repair" in description:
        tags.append("Repair")

    if "soft" in description:
        tags.append("Soft Hair")

    if "shine" in description:
        tags.append("Shiny Hair")

    ##################################################
    # Remove duplicates
    ##################################################

    unique_tags = []

    for tag in tags:

        if tag not in unique_tags:

            unique_tags.append(tag)

    return unique_tags