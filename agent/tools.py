from pymongo import MongoClient, MongoClient

from objects.Order import Order
from objects.OrderItem import OrderItem
from objects.Product import Product

from langchain.tools import tool

import datetime

connection_string = "mongodb://localhost:27017/"

@tool("load_products", return_direct=False)
def load_products() -> list[Product]:
    '''
    Load all products from the MongoDB database.
    Args:
        connection_string: MongoDB connection URI.
    Returns:
        A list of Product objects representing the products in the database.'''

    client = MongoClient(connection_string)
    db = client["TestAgentDataBase"]
    products_collection = db["Products"]

    products: list[Product] = []
    for doc in products_collection.find():
        product = Product(
            product_id=doc['product_id'],
            product_name=doc['product_name'],
            category=doc['category'],
            price_usd=doc['price_usd'],
            inventory=doc['inventory'],
            brand=doc['brand'],
            rating=doc['rating']
        )
        products.append(product)

    return {"result": products}

order_schema = {
    "type": "object",
    "properties": {
        "subtotal_usd": {"type": "number", "minimum": 0},
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "pattern": "^P\\d{4}$"},
                    "quantity": {"type": "integer", "minimum": 1},
                    "unit_price_usd": {"type": "number", "minimum": 0},
                },
                "required": ["product_id", "quantity", "unit_price_usd"]
            }
        }
    },
    "required": ["subtotal_usd", "products"]
}

@tool("add_order", return_direct=True, args_schema=order_schema)
def add_order(subtotal_usd: float, products: list) -> dict:
    """Use this tool second to insert a new order and its line items into MongoDB.

    Args:
        connection_string: MongoDB connection URI.
        order: Order object containing order details and products.
    """
    client = MongoClient(connection_string)
    db = client["TestAgentDataBase"]
    orders_collection = db["Orders"]
    orders_products_collection = db["OrdersProducts"]

    order_id = f"O{str(orders_collection.count_documents({}) + 1).zfill(4)}"
    order_date = datetime.datetime.now().isoformat()
    status = "Processing"
    shipping_usd = 5.99

    # Insert the order into the Orders collection
    order_doc = {
        "order_id": order_id,
        "order_date": order_date,
        "status": status,
        "subtotal_usd": subtotal_usd,
        "shipping_usd": shipping_usd,
        "total_usd": subtotal_usd + shipping_usd
    }
    orders_collection.insert_one(order_doc)

    # Insert the associated products into the OrdersProducts collection
    for item in products:
        op_doc = {
            "order_id": order_id,
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "unit_price_usd": item["unit_price_usd"],
            "line_total_usd": item['quantity'] * item['unit_price_usd']
        }
        orders_products_collection.insert_one(op_doc)

    return {"message": f"Order {order_id} added successfully."}