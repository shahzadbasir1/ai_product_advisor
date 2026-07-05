def calculate_catalog_score(health):

    print("=" * 50)
    print("CATALOG SCORE FILE LOADED")
    print(__file__)
    print("=" * 50)

    score = 100

    deductions = {

        "missing_image": 8,
        "missing_description": 10,
        "missing_url": 6,
        "missing_tags": 5,
        "missing_product_type": 4,
        "missing_inventory": 2

    }

    score -= health["missing_image"] * deductions["missing_image"]

    score -= health["missing_description"] * deductions["missing_description"]

    score -= health["missing_url"] * deductions["missing_url"]

    score -= health["missing_tags"] * deductions["missing_tags"]

    score -= health["missing_product_type"] * deductions["missing_product_type"]

    score -= health["missing_inventory"] * deductions["missing_inventory"]

    score = max(score, 0)

    if score >= 90:
        rating = "★★★★★ Excellent"

    elif score >= 75:
        rating = "★★★★☆ Good"

    elif score >= 60:
        rating = "★★★☆☆ Fair"

    else:
        rating = "★★☆☆☆ Needs Improvement"

    return {

        "score": score,

        "rating": rating

    }
    print("=" * 60)
    print("calculate_catalog_score() called")
    print(type(health))
    print(health)
    print("=" * 60)
    import inspect
    print(inspect.signature(calculate_catalog_score))
    

