from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.tools import load_products
from utils.utils import load_products, load_orders, load_favorite_products

from objects.Order import Order
from objects.Product import Product
from objects.OrderItem import OrderItem

from agent.agent import Agent

app = FastAPI(title='Order Service')

connection_string = "mongodb://localhost:27017/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

agent = Agent()  # Initialize the agent with the appropriate LLM

@app.get('/orders', response_model=list[Order])
def get_orders() -> list[Order]:
    """Return order records from the Orders collection."""
    return load_orders(connection_string)

@app.get('/products', response_model=list[Product])
def get_products() -> list[Product]:
    """Return product records from the Products collection."""
    return load_products(connection_string)

@app.get('/favorites', response_model=list[Product])
def get_favorite_products() -> list[Product]:
    """Return favorite product records from the Favorites collection."""
    return load_favorite_products(connection_string)

@app.post('/query')
def query_agent(query: QueryRequest):
    """Endpoint to receive queries from the agent."""
    # For demonstration, we just print the query. In a real application, you would process it.
    print(f"Received query: {query.query}")

    # Call the agent here and pass the query to it, then return the agent's response.
    response = agent.process_query(query.query)

    return str(response)

# Start the server with: 
# 1. source ./.venv/bin/activate
# 2. python3.12 -m uvicorn server.api:app --reload