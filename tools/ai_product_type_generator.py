from openai import OpenAI
from models.product import Product

client = OpenAI()


def generate_product_type(product: Product) -> str:

    prompt = f"""
You are an e-commerce product catalog specialist.

Determine the most appropriate Product Type for the following product.

Product information:
Title: {product.title or ""}
Vendor: {product.vendor or ""}
Category: {product.category or ""}
Description: {product.description or ""}
Tags: {", ".join(product.tags) if product.tags else ""}

Requirements:
- Use all available product information to determine the Product Type.
- Return a concise, standard e-commerce Product Type.
- Use the appropriate level of specificity.
- Do not use marketing language in the Product Type.
- Do not invent product attributes or claims.
- Do not return a sentence or explanation.
- Return ONLY the Product Type.
- If the available information is insufficient to determine the Product Type, return "Other".

Examples of appropriate Product Types:
Shampoo
Dry Shampoo
Conditioner
Hair Serum
Running Shoes
Laptop
Computer Monitor
Coffee Maker
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    product_type = response.output_text.strip()

    return product_type