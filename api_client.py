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