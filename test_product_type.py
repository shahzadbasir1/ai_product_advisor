from models.product import Product
from tools.ai_product_type_generator import generate_product_type

product = Product(
    product_id="TEST001",
    title="Serene Scalp Oil Control Dry Shampoo Powder",
    description="An ultra-absorbing dry shampoo powder designed to absorb excess oil and refresh the scalp between washes.",
    vendor="Oribe",
    category="Hair Care",
    price=42.00,
    status="active",
    tags=["oil control", "scalp care", "dry shampoo"],
    source_catalog_id="TEST"
)


product_type = generate_product_type(product)

print("Generated Product Type:")
print(product_type)