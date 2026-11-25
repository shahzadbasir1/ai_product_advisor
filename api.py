from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from models.product import Product
from ingestion.shopify_loader import load_shopify_products

from tools.ai_description_generator import generate_description

from tools.ai_product_type_generator import generate_product_type
from tools.ai_tag_generator import generate_tags

from pathlib import Path
import shutil

#from rag.knowledge_base import index_document
from rag.knowledge_base import (
    index_document,
    list_knowledge_documents
)

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

@app.get("/shopify/products")
def get_shopify_products(limit: int = 50):

    if limit < 1 or limit > 250:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 250"
        )

    try:
        products = load_shopify_products(
            limit=limit
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load Shopify products: {exc}"
        )

    return {
        "source": "shopify",
        "count": len(products),
        "products": [
            product.model_dump(mode="json")
            for product in products
        ]
    }

@app.post("/knowledge/upload")
def upload_knowledge_document(
    merchant_id: str = Form(...),
    file: UploadFile = File(...)
):
    merchant_id = merchant_id.strip().lower()

    if not merchant_id:
        raise HTTPException(
            status_code=400,
            detail="merchant_id is required"
        )

    filename = Path(file.filename or "").name

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required"
        )

    allowed_extensions = {
        ".txt",
        ".pdf",
        ".docx"
    }

    extension = Path(filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Supported knowledge document types are .txt, .pdf, and .docx"
        )

    allowed_extensions = {
        ".txt",
        ".pdf",
        ".docx"
    }

    extension = Path(filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Supported knowledge document types are .txt, .pdf, and .docx"
        )

    knowledge_dir = Path("data/knowledge") / merchant_id
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    file_path = knowledge_dir / filename

    try:
        with file_path.open("wb") as destination:
            shutil.copyfileobj(file.file, destination)

        chunks_indexed = index_document(
            str(file_path),
            merchant_id=merchant_id
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index knowledge document: {exc}"
        )

    finally:
        file.file.close()

    return {
        "status": "indexed",
        "merchant_id": merchant_id,
        "document": filename,
        "chunks_indexed": chunks_indexed
    }

@app.get("/knowledge/documents")
def get_knowledge_documents(
    merchant_id: str
):
    merchant_id = merchant_id.strip().lower()

    if not merchant_id:
        raise HTTPException(
            status_code=400,
            detail="merchant_id is required"
        )

    documents = list_knowledge_documents(
        merchant_id
    )

    return {
        "merchant_id": merchant_id,
        "documents": documents
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