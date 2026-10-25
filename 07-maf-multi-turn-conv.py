import asyncio
import os
import sys
from agent_framework.foundry import FoundryChatClient
from agent_framework import Agent, Message
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv


load_dotenv()


def validate_environment_variables():
    """Validate that required environment variables are set."""
    model = os.getenv("FOUNDRY_MODEL_NAME")
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")

    if not model:
        raise ValueError("FOUNDRY_MODEL_NAME environment variable is not set")
    if not endpoint:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT environment variable is not set")

    return model, endpoint


async def main(model: str, endpoint: str):
    async with DefaultAzureCredential() as credential:
        chat_client = FoundryChatClient(
            credential=credential,
            model=model,
            project_endpoint=endpoint,
        )

        agent = Agent(
            client=chat_client,
            name="general-agent",
            description="general chat demo agent",
            instructions=(
                "You are a helpful general support assistant. "
                "When a user asks a question, keep your responses clear and concise."
            ),
        )
        session = agent.create_session()

        while True:
            try:
                # input() blocks, so run it in a worker thread to keep the event loop free
                user_input = await asyncio.to_thread(
                    input, "You (type 'exit' to quit): "
                )
            except EOFError:
                break

            user_input = user_input.strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                break

            try:
                resp = await agent.run(
                    Message(role="user", contents=user_input), session=session
                )
                print(f"Agent: {resp.text}\n")
            except Exception as e:
                print(f"Error: {type(e).__name__}: {e}\n", file=sys.stderr)


if __name__ == "__main__":
    try:
        model_name, project_endpoint = validate_environment_variables()
    except ValueError as e:
        sys.exit(f"Configuration error: {e}")

    try:
        asyncio.run(main(model_name, project_endpoint))
    except KeyboardInterrupt:
        print("\nGoodbye!")
