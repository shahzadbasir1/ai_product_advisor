from fastapi import FastAPI
from models.product import Product
from tools.ai_description_generator import generate_description

from tools.ai_product_type_generator import generate_product_type
from tools.ai_tag_generator import generate_tags

app = FastAPI(
    title="AI Product Advisor API",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "message": "AI Product Advisor API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.post("/generate-description")
def api_generate_description(product: Product):

    description = generate_description(product)

    return {
        "product_id": product.product_id,
        "description": description
    }

@app.post("/generate-product-type")
def api_generate_product_type(product: Product):

    product_type = generate_product_type(product)

    return {
        "product_id": product.product_id,
        "product_type": product_type
    }

@app.post("/generate-tags")
def api_generate_tags(product: Product):

    tags = generate_tags(product)

    return {
        "product_id": product.product_id,
        "tags": tags
    }