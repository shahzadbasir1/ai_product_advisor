from openai import OpenAI
from models.product import Product

client = OpenAI()


def generate_tags(product: Product):

    prompt = f"""
You are an e-commerce SEO specialist.

Generate SEO-friendly tags for the following product.

Product information:
Title: {product.title or ""}
Vendor: {product.vendor or ""}
Category: {product.category or ""}
Product Type: {product.product_type or ""}
Description: {product.description or ""}

Requirements:
- Generate 5-10 concise SEO tags.
- Base every tag only on the supplied product information.
- Include relevant product type, category, use case, and customer-search terms.
- Do not invent product attributes or claims.
- Avoid duplicate or near-duplicate tags.
- Do not use hashtags.
- Return ONLY a comma-separated list of tags.
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    raw_tags = response.output_text.strip()

    tags = [
        tag.strip()
        for tag in raw_tags.split(",")
        if tag.strip()
    ]

    return tags