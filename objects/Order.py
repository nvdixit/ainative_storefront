from pydantic import BaseModel
from objects.OrderItem import OrderItem
import datetime

class Order(BaseModel):
    order_id: str
    order_date: datetime.datetime
    status: str
    subtotal_usd: float
    shipping_usd: float
    total_usd: float
    products: list[OrderItem] = []
