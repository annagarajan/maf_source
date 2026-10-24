import asyncio
import os
from agent_framework.foundry import FoundryChatClient
from agent_framework import Agent, Message
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


load_dotenv()

credentials = DefaultAzureCredential()
chat_client = FoundryChatClient(
    credential = credentials,
    model= os.getenv("FOUNDRY_MODEL_NAME"),
    project_endpoint= os.getenv("FOUNDRY_PROJECT_ENDPOINT")
)

async def main():
    
    agent = Agent(
        client= chat_client,
        name="general-agent",
        description="general chat demo agent",
        instructions=(
            "You are a helpful general support assistant. "
            "When a user asks a question, Keep your responses clear and concise."
        )
    )
    session = agent.create_session()
    while True:
        user_input= input("You : (type 'exit to quit) :")
        if user_input.strip().lower() in ["exit","quit"]:
            break

        resp = await agent.run(Message(role="user", contents=user_input), session=session)
        print(f"Agent : {resp.text}")

if __name__ == "__main__":
    asyncio.run(main())

    
    