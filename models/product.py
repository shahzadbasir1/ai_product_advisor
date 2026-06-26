from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductVariant(BaseModel):
    sku: str
    name: str
    price: float


class Product(BaseModel):

    # Required Fields
    product_id: str
    title: str
    description: str

    vendor: str
    category: str

    price: float

    status: str

    # Optional Fields
    product_url: Optional[str] = None

    handle: Optional[str] = None

    product_type: Optional[str] = None

    tags: List[str] = Field(default_factory=list)

    inventory_qty: Optional[int] = None

    compare_at_price: Optional[float] = None

    image_url: Optional[str] = None

    published: Optional[bool] = None

    variants: List[ProductVariant] = Field(default_factory=list)

    # Audit Fields
    source_catalog_id: str

    updated_datetime: Optional[datetime] = None

    updated_by: Optional[str] = None