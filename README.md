# MAF Source (Multi-Agent Framework)

A collection of examples demonstrating how to use the Microsoft Foundry Agent Framework for building AI-powered agents.

## Overview

This repository contains progressive examples of building agents with Azure OpenAI and Microsoft Foundry, from basic chat clients to multi-turn conversations with agents.

## Files

- **01-maf-openai.py** - Basic OpenAI chat client example
- **02-maf-azopenai.py** - Azure OpenAI chat client example
- **03-maf-azfoundry.py** - Azure Foundry chat client example
- **04-maf-azfndry_agent.py** - Azure Foundry agent example
- **05-maf-message-class.py** - Message class examples
- **06-maf-tool-deco.py** - Tool decorator examples
- **07-maf-multi-turn-conv.py** - Multi-turn conversation example with persistent sessions

## Requirements

```
pip install agent-framework
```

Also requires:
- Azure credentials (DefaultAzureCredential)
- Environment variables for Foundry configuration (see .env.example)

## Quick Start

### Multi-Turn Conversation Example

Run the multi-turn conversation agent:

```bash
python 07-maf-multi-turn-conv.py
```

This launches an interactive agent that maintains conversation history across multiple turns.

### Environment Setup

Create a `.env` file with:
```
FOUNDRY_MODEL_NAME=<your-model>
FOUNDRY_PROJECT_ENDPOINT=<your-endpoint>
```

## Key Features

- Multi-turn conversation support with session management
- Azure Foundry integration
- DefaultAzureCredential authentication
- Agent framework with customizable instructions and descriptions
