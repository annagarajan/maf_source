import asyncio
import os
from agent_framework import Agent, Message
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

credentials = DefaultAzureCredential()
    
client = FoundryChatClient(
    credential= credentials,
    project_endpoint= os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
    model=os.getenv("FOUNDRY_MODEL_NAME")
)

async def main():

    agent = client.as_agent(
                   name="IT Help Desk Agent",
                   instructions= """
                        You are a helpful IT support assistant for a company.
                        When a user asks a question, use the available tools to find the answer.
                        Always use a tool before responding — do not answer from memory alone.
                        Keep your responses clear and concise.
                       
                   """,
                   description= """
                       Provides IT support by troubleshooting technical issues,
                       answering questions about company IT policies, and helping
                       employees resolve hardware, software, network, and account-access problems.
                   """
           )
    user_message = Message(role="user", contents= ["Provide me simple steps to reset the password"])
    resp = await agent.run(user_message)
    print(resp.text)


if __name__ == "__main__":
    asyncio.run(main())
    

