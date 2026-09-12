import os
from openai import OpenAI
from models.product import Product
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_description(product: Product) -> str:

    prompt = f"""
You are an expert e-commerce product content writer.

Generate a clear, compelling, customer-friendly product description
using ONLY the product information provided below.

Product information:
Title: {product.title or ""}
Vendor: {product.vendor or ""}
Category: {product.category or ""}
Product Type: {product.product_type or ""}
Existing Description: {product.description or ""}
Tags: {", ".join(product.tags) if product.tags else ""}

Requirements:
- Write 1-2 concise paragraphs.
- Clearly explain what the product is and its key benefits.
- Use professional e-commerce language.
- Improve weak or incomplete source descriptions.
- Do not invent ingredients, specifications, certifications, claims,
  or benefits that are not supported by the supplied product data.
- Do not include SEO tags or headings.
- Return only the improved product description.
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return response.output_text.strip()