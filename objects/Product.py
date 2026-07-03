from pydantic import BaseModel

class Product(BaseModel):
    product_id: str
    product_name: str
    category: str
    price_usd: float
    inventory: int
    brand: str
    rating: float