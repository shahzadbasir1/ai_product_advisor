import os
from openai import OpenAI
from models.product import Product
from dotenv import load_dotenv
from rag.knowledge_base import search_knowledge

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_description(product: Product) -> str:

    knowledge_query = f"""
    Product description guidelines for:
    Vendor: {product.vendor or ""}
    Category: {product.category or ""}
    Product Type: {product.product_type or ""}
    """

    merchant_id = (product.vendor or "").strip().lower()

    knowledge_results = search_knowledge(
        knowledge_query,
        merchant_id=merchant_id,
        n_results=2
    )

    merchant_guidelines = "\n\n".join(
        result["document"]
        for result in knowledge_results
    )

    prompt = f"""
You are an expert e-commerce product content writer.

Generate a clear, compelling, customer-friendly product description
using the Product Information and Merchant Guidelines below.

IMPORTANT GROUNDING RULES:

1. PRODUCT INFORMATION is the factual source of truth for this specific product.
2. Only make product-specific claims that are directly supported by the
   Product Information.
3. Do not infer or invent ingredients, features, specifications, certifications,
   performance claims, health claims, results, or benefits that are not supported
   by the Product Information.
4. MERCHANT GUIDELINES are writing and policy instructions. They may control
   tone, style, length, terminology, SEO approach, and prohibited claims.
5. Do NOT treat Merchant Guidelines as evidence that this specific product
   has a particular ingredient, feature, benefit, or performance characteristic.
6. If the Product Information is limited, write a useful but conservative
   description rather than filling gaps with assumptions.

Product Information:
Title: {product.title or ""}
Vendor: {product.vendor or ""}
Category: {product.category or ""}
Product Type: {product.product_type or ""}
Existing Description: {product.description or ""}
Tags: {", ".join(product.tags) if product.tags else ""}

Merchant Guidelines:
{merchant_guidelines}

    Requirements:
    - Follow the Merchant Guidelines when they are relevant to this product.
    - Clearly explain what the product is using only supported product facts.
    - Use professional, polished e-commerce language suitable for direct publication.
    - Improve weak or incomplete source descriptions without introducing unsupported facts.
    - Do not include SEO tags or headings.
    - Do not include analysis, reasoning, commentary, drafting notes, editing notes,
      word-count calculations, questions, self-critique, or instructions.
    - Do not discuss whether a claim is supported or unsupported in the output.
    - Do not include phrases such as "unsupported", "remove", "need", "word count",
      or other internal drafting commentary.
    - The response must contain ONLY the final customer-facing product description.
    - The response must be ready to publish without further cleanup.
"""
    
    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return response.output_text.strip()