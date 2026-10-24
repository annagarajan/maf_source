import asyncio
import os
from agent_framework.foundry import FoundryChatClient
from agent_framework import Agent, tool, Message
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from random import randint

load_dotenv()

@tool
async def get_weather(location :str) -> str: 
    """
    Get weather for a location

    Args : 
        location: city or location name to get weather details

    returns:
        A string describing the current weather details.

    """
    conditions = ["sunny", "rainy","rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0,3)]} with a high of {randint(10,30)} °C"
    
    

async def main():
    credentials = DefaultAzureCredential()
    client_chat = FoundryChatClient(
        credential= credentials,
        project_endpoint= os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model=os.getenv("FOUNDRY_MODEL_NAME")
    )

    agent = Agent(
            client = client_chat,
            name ="simple-tool-agent",
            description="Get generic information like weather , products etc.,",
            instructions=(
                "You are a helpful general support assistant. "
                "When a user asks a question, use the available tools to find the answer. "
                "Always use a tool before responding — do not answer from memory alone. "
                "Keep your responses clear and concise."
            ),
            tools=[get_weather]
    )

    # location = input("enter the city/location :").strip()

    while True:
        user_input = input("You (type 'exit' to quit): ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        resp = await agent.run(Message(role="user", contents=user_input))
        print("Agent:", resp.text)



if __name__ == "__main__":
    asyncio.run(main())

