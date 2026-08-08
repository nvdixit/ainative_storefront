from pymongo import MongoClient, MongoClient

from objects.Order import Order
from objects.OrderItem import OrderItem
from objects.Product import Product
from agent.schemas import ORDER_SCHEMA, FAVORITE_SCHEMA

from langchain.tools import tool

import datetime

connection_string = "mongodb://localhost:27017/"

@tool("load_products", return_direct=False)
def load_products() -> list[Product]:
    '''
    Use this tool to extract all products available for purchase.
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


@tool("add_favorite_product", return_direct=True, args_schema=FAVORITE_SCHEMA)
def add_favorite_product(product_ids: list[str]) -> dict:
    """Use this tool to add products to the Favorites list of the user after looking up
    the product IDs in the Products collection. This tool should be called after load_products to ensure that the product IDs are valid.

    Args:
        product_ids: List of product IDs to be added to favorites.
    """
    client = MongoClient(connection_string)
    db = client["TestAgentDataBase"]
    favorites_collection = db["Favorites"]
    products_collection = db["Products"]

    for product_id in product_ids:
        favorite = products_collection.find_one({"product_id": product_id})
        exists = favorites_collection.find_one({"product_id": product_id})

        if not exists:
            favorites_collection.insert_one(favorite)
        else:
            return {"message": f"Looks like {product_id} is already in your favorites!"}

    return {"message": f"Products {', '.join(product_ids)} added to favorites successfully."}


@tool("add_order", return_direct=True, args_schema=ORDER_SCHEMA)
def add_order(subtotal_usd: float, products: list) -> dict:
    """Use this tool second after load_products to insert a new order and its line items into the database.
       Do not add extra products to the order. Only add the products that the user has requested.

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

    return {"message": f"Ok, I ordered that for you! You can check {order_id} in your order history!"}