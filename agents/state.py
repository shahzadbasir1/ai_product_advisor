from typing import TypedDict
from models.product import Product

class ProductWorkflowState(TypedDict):

#    product: Product
    product: object

    review: dict

    description: str

    tags: list

    success: bool