import os
from typing import List

import requests
from dotenv import load_dotenv

from models.product import Product, ProductVariant


load_dotenv(override=True)


SHOPIFY_API_VERSION = "2026-07"


def get_shopify_access_token() -> str:
    """
    Get a temporary Shopify Admin API access token
    using the client credentials grant.
    """

    shop = os.getenv("SHOPIFY_STORE_DOMAIN")
    client_id = os.getenv("SHOPIFY_CLIENT_ID")
    client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")

    if not shop:
        raise ValueError(
            "SHOPIFY_STORE_DOMAIN is not configured."
        )

    if not client_id:
        raise ValueError(
            "SHOPIFY_CLIENT_ID is not configured."
        )

    if not client_secret:
        raise ValueError(
            "SHOPIFY_CLIENT_SECRET is not configured."
        )

    token_url = (
        f"https://{shop}/admin/oauth/access_token"
    )

    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    access_token = data.get("access_token")

    if not access_token:
        raise RuntimeError(
            "Shopify did not return an access token."
        )

    return access_token


def load_shopify_products(
    limit: int = 50
) -> List[Product]:
    """
    Load products from Shopify and convert them
    into AI Product Advisor Product objects.
    """

    shop = os.getenv("SHOPIFY_STORE_DOMAIN")

    if not shop:
        raise ValueError(
            "SHOPIFY_STORE_DOMAIN is not configured."
        )

    access_token = get_shopify_access_token()

    graphql_url = (
        f"https://{shop}/admin/api/"
        f"{SHOPIFY_API_VERSION}/graphql.json"
    )

    query = """
    query GetProducts($first: Int!) {
      products(first: $first) {
        nodes {
          id
          title
          handle
          description
          vendor
          productType
          status
          tags
          totalInventory

          category {
            id
            name
            fullName
          }

          priceRangeV2 {
            minVariantPrice {
              amount
              currencyCode
            }
          }

          featuredMedia {
            ... on MediaImage {
              image {
                url
                altText
              }
            }
          }

          variants(first: 100) {
            nodes {
              id
              title
              sku
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    """

    response = requests.post(
        graphql_url,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
        json={
            "query": query,
            "variables": {
                "first": limit
            },
        },
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if result.get("errors"):
        raise RuntimeError(
            f"Shopify GraphQL error: "
            f"{result['errors']}"
        )

    shopify_products = (
        result["data"]["products"]["nodes"]
    )

    products = []

    for item in shopify_products:

        category = item.get("category")

        category_name = (
            category.get("fullName", "")
            if category
            else ""
        )

        featured_media = item.get(
            "featuredMedia"
        )

        image_url = None

        if (
            featured_media
            and featured_media.get("image")
        ):
            image_url = (
                featured_media["image"].get("url")
            )

        variant_objects = []

        for variant in item["variants"]["nodes"]:

            variant_objects.append(
                ProductVariant(
                    sku=variant.get("sku") or "",
                    name=variant.get("title") or "",
                    price=float(
                        variant.get("price") or 0
                    ),
                )
            )

        price = float(
            item["priceRangeV2"]
            ["minVariantPrice"]
            ["amount"]
        )

        product = Product(
            product_id=item["id"],
            title=item.get("title") or "",
            description=(
                item.get("description") or ""
            ),
            vendor=item.get("vendor") or "",
            category=category_name,
            price=price,
            status=item.get("status") or "",
            handle=item.get("handle"),
            product_type=(
                item.get("productType") or None
            ),
            tags=item.get("tags") or [],
            inventory_qty=(
                item.get("totalInventory")
            ),
            image_url=image_url,
            source_catalog_id=(
                f"shopify:{shop}"
            ),
            variants=variant_objects,
        )

        products.append(product)

    return products