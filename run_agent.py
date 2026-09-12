import logging
import os

os.makedirs(
    "logs",
    exist_ok=True
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(
            "logs/workflow.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

from storage.catalog_repository import (
    load_catalog,
    save_catalog
)

from agents.product_workflow import graph
from tools.ai_product_reviewer import review_product

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

CATALOG_FILE = "data/catalogs/test_products.json"

products = load_catalog(CATALOG_FILE)
logging.info(
    f"{len(products)} products loaded"
)
print(f"{len(products)} products loaded")

#commented 07/10/26
# product = products[0]

# print(f"Testing Product: {product.product_id}")

# review = review_product(product)

# print(review)
#commented 07/10/26
for product in products:

    print(f"Processing {product.product_id}")
    logging.info(
         f"Processing {product.product_id}"
    )

    result = graph.invoke(
        {
            "product": product,
            "review": {},
            "description": "",
            "tags": [],
            "success": False
        }
    )
    
    if result["success"]:

        logging.info(
            f"Completed {product.product_id}"
        )

save_catalog(
    products,
    CATALOG_FILE
)

print("Done.")
logging.info(
    "Finished."
)