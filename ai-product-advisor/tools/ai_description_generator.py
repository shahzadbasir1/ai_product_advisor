from models.product import Product


def generate_description(product: Product) -> str:

    title = product.title or "Product"

    vendor = product.vendor or "Unknown Brand"

    category = product.category or "General"

    product_type = product.product_type or "Product"

    tags = ", ".join(product.tags) if product.tags else ""

    description = f"""
{title} by {vendor} is a premium {product_type.lower()} designed for customers looking for high-quality {category.lower()} products.

This product helps improve overall hair health while providing excellent performance and long-lasting results. It is suitable for everyday use and works well for customers seeking healthier, softer and more manageable hair.

Key Benefits

• Nourishes and protects hair
• Helps improve appearance and texture
• Suitable for regular use
• High quality ingredients
• Trusted {vendor} quality

Recommended For

Customers looking for reliable {category.lower()} solutions.

Keywords: {tags}
"""

    return description.strip()