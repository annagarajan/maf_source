import os
import asyncio
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

async def main():
    credential = DefaultAzureCredential()
    client = FoundryChatClient(
        project_endpoint= os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model= os.getenv("FOUNDRY_MODEL_NAME"),
        credential= credential
    )

    agent = client.as_agent(
        name="AZ OpenAI MAF Agent",
        instructions="You are helpful assistant that generates MAF files based on user input.",
    )

    resp = await agent.run("What is the capital of India")
    print(resp.text)

if __name__ == "__main__":
    asyncio.run(main())