from pydantic import BaseModel, Field
import json

from langchain.agents import create_agent

from agent.tools import load_products, add_order

class Agent:
    class CustomResponse(BaseModel):
        message: str = Field(description="Whether the order was added successfully or not")

    def __init__(self):
        # Load the prompt form add_order.md and set it as the system prompt for the agent
        with open("agent/add_order.md", "r") as f:
            system_prompt = f.read()

        # Keep the temperature low for more deterministic responses and reliable tool calling
        self.agent = create_agent(model="ollama:gemma4", 
                                  tools=[load_products, add_order], 
                                  system_prompt=system_prompt,
                                  response_format=self.CustomResponse)
        
    def process_query(self, query):
        print("calling the agent with query:", query)  # Log the incoming query for debugging purposes

        # Set up system instructions
        full_query = {"messages": [{"role": "user", "content": query}]}
        result = self.agent.invoke(
            full_query
        )

        agent_response = (result["messages"][-1]).content
        agent_response_json = json.loads(agent_response)

        return agent_response_json["message"]



