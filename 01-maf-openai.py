import asyncio
from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatClient

load_dotenv()

async def main():
    agent = OpenAIChatClient().as_agent(
        name="OpenAI MAF Agent",
        instructions="You are helpful assistant that generates MAF files based on user input."
    )

    resp = await agent.run("What is capital of india")
    print(resp.text)

if __name__ == "__main__":
    asyncio.run(main())



