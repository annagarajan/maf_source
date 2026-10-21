import asyncio
import os
from azure.identity.aio import AzureCliCredential
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()

async def main():
    client = OpenAIChatClient(
        model= os.getenv("AZURE_OPENAI_DEPLOYMENT_MODEL"),
        azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
    ).as_agent(
        name="AZ OpenAI MAF Agent",
        instructions="You are helpful assistant that generates MAF files based on user input."
    )
    resp =await client.run("What is the capital on India")
    print(resp.text)


if __name__ == "__main__":
    asyncio.run(main())

  