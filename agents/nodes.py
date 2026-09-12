import logging

from tools.ai_product_reviewer import review_product
from tools.ai_description_generator import generate_description
from tools.ai_tag_generator import generate_tags
from datetime import datetime



logger = logging.getLogger(__name__)


############################################################
# Review Product
############################################################

def review_node(state):

    product = state["product"]

    logger.info(
        f"Reviewing {product.product_id}"
    )

    review = review_product(product)

    state["review"] = review

    return state


############################################################
# Generate Description
############################################################

def description_node(state):

    product = state["product"]

    logger.info(
        f"Generating Description {product.product_id}"
    )

    description = generate_description(product)

    state["description"] = description
    # state = {

    #     "product": product,

    #     "review": review,

    #     "description": description,

    #     "tags": tags,

    #     "success": True
    # }

    return state


############################################################
# Generate SEO Tags
############################################################

def tags_node(state):

    product = state["product"]

    logger.info(
        f"Generating Tags {product.product_id}"
    )

    if state["description"]:

        product.description = state["description"]

    tags = generate_tags(product)

    description = state["description"]

    if tags:
        description += (
            "\n\nKeywords: "
            + ", ".join(tags)
        )

    state["description"] = product.description
    state["tags"] = tags

    return state


############################################################
# Save Product
############################################################

def save_node(state):

    product = state["product"]

    logger.info(
        f"Saving {product.product_id}"
    )

    if state["description"]:

        product.description = state["description"]

    if state["tags"]:

        product.tags = state["tags"]

    state["success"] = True
    product.updated_datetime = datetime.now()

    product.updated_by = "LangGraph Agent"
    return state

############################################################
# Conditional Routing
############################################################

def should_generate_content(state):

    review = state["review"]

    score = review["score"]

    weaknesses = review["weaknesses"]

    logger.info(
        f"Review Score = {score}"
    )

    logger.info(
        f"Weaknesses: {weaknesses}"
    )

    if score >= 90:

        logger.info(
            "Product already looks good. Skipping AI generation."
        )

        return "save"

    if len(weaknesses) == 0:

        logger.info(
            "No weaknesses found. Skipping AI generation."
        )

        return "save"

    logger.info(
        "Product requires AI enrichment."
    )

    return "description"