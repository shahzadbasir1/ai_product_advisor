from models.product import Product


def calculate_product_score(product: Product):

    image_score = 0
    description_score = 0
    seo_score = 0
    metadata_score = 0
    completeness_score = 0

    recommendations = set()

    if product.image_url:
        image_score = 20
    else:
        recommendations.add(
            "Upload a product image."
        )

    if product.description:

        length = len(product.description)

        if length > 150:
            description_score = 20

        elif length > 80:
            description_score = 15
            recommendations.add(
                "Expand the product description."
            )

        else:
            description_score = 8
            recommendations.add(
                "Improve the product description."
            )        

##################################################
# SEO Score
##################################################

    seo_score = 0

    # Product URL
    if product.product_url:
        seo_score += 10
    else:
        recommendations.add(
            "Add a product URL."
        )

    # SEO Tags
    if not product.tags:

        recommendations.add(
            "Generate SEO tags."
        )

    elif len(product.tags) < 5:

        seo_score += 5

        recommendations.add(
            "Add more SEO tags."
        )

    else:

        seo_score += 10
        
    metadata_fields = [
        product.vendor,
        product.category,
        product.product_type,
        product.price,
        product.inventory_qty
    ]

    filled = sum(bool(f) for f in metadata_fields)

    metadata_score = int(
        (filled / len(metadata_fields)) * 20
    )

    if filled < len(metadata_fields):

        recommendations.add(
            "Complete the product metadata."
        )

    # ---------- Completeness Score ----------

    completeness_fields = [
        product.title,
        product.description,
        product.vendor,
        product.category,
        product.product_type,
        product.image_url,
        product.product_url,
        product.tags
    ]

    filled = sum(bool(f) for f in completeness_fields)

    completeness_score = int(
        (filled / len(completeness_fields)) * 20
    )

    # ---------- Overall Score ----------

    overall_score = (
        image_score
        + description_score
        + seo_score
        + metadata_score
        + completeness_score
    )

    return {

        "overall_score": overall_score,

        "image_score": image_score,

        "description_score": description_score,

        "seo_score": seo_score,

        "metadata_score": metadata_score,

        "completeness_score": completeness_score,

        "recommendations": sorted(recommendations)
    }        