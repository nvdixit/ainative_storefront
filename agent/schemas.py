# Schema for valid order insert
ORDER_SCHEMA = {
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

# Schema for valid favorite product insert
FAVORITE_SCHEMA = {
    "type": "object",
    "properties": {
        "product_ids": {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^P\\d{4}$"
            },
            "required": ["product_ids"]
        }
    },
    "required": ["product_ids"]
}