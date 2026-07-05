from urllib.parse import quote


def get_image_search_url(product):

    query = " ".join(
        filter(
            None,
            [
                product.vendor,
                product.title,
                product.product_type
            ]
        )
    )

    return (
        "https://www.google.com/search?tbm=isch&q="
        + quote(query)
    )