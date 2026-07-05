from analysis.product_score import calculate_product_score


def review_product(product):
    print("NEW review_product() is executing")

    score = calculate_product_score(product)

    strengths = []
    weaknesses = []
    recommendations = []

    ##################################################
    # Image
    ##################################################

    if product.image_url:
        strengths.append(
            "Product image uploaded."
        )
    else:
        weaknesses.append(
            "No product image."
        )
        recommendations.append(
            "Upload a product image."
        )

    ##################################################
    # Description
    ##################################################

    if product.description and len(product.description) > 150:
        strengths.append(
            "High-quality product description."
        )
    else:
        weaknesses.append(
            "Description needs improvement."
        )
        recommendations.append(
            "Generate a richer product description."
        )

    ##################################################
    # Product URL
    ##################################################

    if product.product_url:
        strengths.append(
            "Product URL available."
        )
    else:
        weaknesses.append(
            "Product URL missing."
        )
        recommendations.append(
            "Add a product URL."
        )

    ##################################################
    # SEO Tags
    ##################################################

    if len(product.tags) >= 5:
        strengths.append(
            "Good SEO tag coverage."
        )
    else:
        weaknesses.append(
            "SEO tags can be improved."
        )
        recommendations.append(
            "Generate more SEO tags."
        )

    ##################################################
    # Product Type
    ##################################################

    if product.product_type:
        strengths.append(
            "Product type specified."
        )
    else:
        weaknesses.append(
            "Product type missing."
        )
        recommendations.append(
            "Specify a product type."
        )

    ##################################################
    # Rating
    ##################################################

    overall = score["overall_score"]

    if overall >= 90:
        rating = "★★★★★ Excellent"
    elif overall >= 75:
        rating = "★★★★☆ Good"
    elif overall >= 60:
        rating = "★★★☆☆ Fair"
    else:
        rating = "★★☆☆☆ Needs Improvement"

    return {

        "rating": rating,

        "score": overall,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations

    }