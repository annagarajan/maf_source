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


async def get_user_input(prompt: str) -> str:
    """Asynchronously get user input without blocking the event loop."""
    return await asyncio.to_thread.run_in_executor(None, input, prompt)


async def main():
    # Validate environment variables
    model, endpoint = validate_environment_variables()

    # Create credentials and client
    credentials = DefaultAzureCredential()
    chat_client = FoundryChatClient(
        credential=credentials,
        model=model,
        project_endpoint=endpoint
    )

    agent = Agent(
        client=chat_client,
        name="general-agent",
        description="general chat demo agent",
        instructions=(
            "You are a helpful general support assistant. "
            "When a user asks a question, keep your responses clear and concise."
        )
    )

    session = agent.create_session()

    try:
        while True:
            try:
                user_input = await get_user_input("You : (type 'exit' to quit): ")
            except EOFError:
                print("\nInput stream closed. Exiting.")
                break
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting.")
                break

            # Skip empty input
            if not user_input.strip():
                continue

            if user_input.strip().lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            try:
                resp = await agent.run(
                    Message(role="user", contents=user_input),
                    session=session
                )
                print(f"Agent: {resp.text}\n")
            except Exception as e:
                print(f"Error while processing response: {type(e).__name__}: {e}")
                print("Please try again.\n")

    finally:
        # Clean up resources
        if hasattr(session, 'close'):
            session.close()
        if hasattr(credentials, 'close'):
            await credentials.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
