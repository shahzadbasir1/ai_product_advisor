from pydantic import BaseModel

class ProductVariant(BaseModel):
    sku: str
    name: str
    price: float