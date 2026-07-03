from pydantic import BaseModel

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    category: str
    brand: str
    price_usd: float
    quantity: int
    unit_price_usd: float
    line_total_usd: float
