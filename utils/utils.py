from pymongo import MongoClient, MongoClient

from objects.Order import Order
from objects.OrderItem import OrderItem
from objects.Product import Product

def load_orders(connection_string) -> list[Order]:
    client = MongoClient(connection_string)
    db = client["TestAgentDataBase"]
    orders_collection = db["Orders"]
    orders_products_collection = db["OrdersProducts"]
    products_collection = db["Products"]

    orders: list[Order] = []
    for doc in orders_collection.find():
        order_id = doc['order_id']
        order_items: list[OrderItem] = []

        order_items = []
        # For each unique order_id, find all associated products in the OrdersProducts collection
        for op_doc in orders_products_collection.find({"order_id": order_id}):

            # For each product_id in the OrdersProducts collection, find the corresponding product details in the Products collection
            for product_doc in products_collection.find({"product_id": op_doc['product_id']}):
                order_item = OrderItem(
                    product_id=op_doc['product_id'],
                    product_name=product_doc['product_name'],
                    category=product_doc['category'],
                    brand=product_doc['brand'],
                    price_usd=product_doc['price_usd'],
                    quantity=op_doc['quantity'],
                    unit_price_usd=op_doc['unit_price_usd'],
                    line_total_usd=op_doc['line_total_usd']
                )
                order_items.append(order_item)

        orders.append(Order(
            order_id=order_id,
            order_date=doc['order_date'],
            status=doc['status'],
            subtotal_usd=doc['subtotal_usd'],
            shipping_usd=doc['shipping_usd'],
            total_usd=doc['total_usd'],
            products=order_items
        ))
    return orders

def load_products(connection_string) -> list[Product]:
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

    return products


def load_favorite_products(connection_string) -> list[Product]:
    '''
    Load favorite products from the MongoDB database.
    Args:
        connection_string: MongoDB connection URI.
    Returns:
        A list of Product objects representing the favorite products in the database.'''
    client = MongoClient(connection_string)
    db = client["TestAgentDataBase"]
    favorites_collection = db["Favorites"]

    favorites: list[Product] = []
    for doc in favorites_collection.find():
        product = Product(
            product_id=doc['product_id'],
            product_name=doc['product_name'],
            category=doc['category'],
            price_usd=doc['price_usd'],
            inventory=doc['inventory'],
            brand=doc['brand'],
            rating=doc['rating']
        )
        favorites.append(product)

    return favorites
