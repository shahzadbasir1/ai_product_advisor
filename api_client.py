import requests


API_BASE_URL = "http://127.0.0.1:8000"


def generate_description_api(product):

    response = requests.post(
        f"{API_BASE_URL}/generate-description",
        json=product.model_dump(mode="json"),
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["description"]

def generate_tags_api(product):

    response = requests.post(
        f"{API_BASE_URL}/generate-tags",
        json=product.model_dump(mode="json"),
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["tags"]


def generate_product_type_api(product):

    response = requests.post(
        f"{API_BASE_URL}/generate-product-type",
        json=product.model_dump(mode="json"),
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["product_type"]

def upload_knowledge_document_api(
    merchant_id,
    uploaded_file
):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "text/plain"
        )
    }

    data = {
        "merchant_id": merchant_id
    }

    response = requests.post(
        f"{API_BASE_URL}/knowledge/upload",
        data=data,
        files=files,
        timeout=60
    )

    response.raise_for_status()

    return response.json()

def list_knowledge_documents_api(
    merchant_id
):
    response = requests.get(
        f"{API_BASE_URL}/knowledge/documents",
        params={
            "merchant_id": merchant_id
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data["documents"]

def load_shopify_products_api(limit=50):

    response = requests.get(
        f"{API_BASE_URL}/shopify/products",
        params={
            "limit": limit
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["products"]