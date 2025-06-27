# Workshop on LangGraph & LangFuse

In this workshop, we'll be going from the [Osedea Hackaton Boilerplate](https://github.com/rangzen/osedea-hackaton-2025-boilerplate) LangGraph example (~almost) to a LangFuse integrated example. We'll touch on basic agents, patterns and observability. The project is setup in multiple steps to easily create diffs and see what changes between each steps. 

Steps:

1. The initial example is a linear workflow with LangGraph that uses Wikipedia and Tavily as nodes in the graph.
1. We add a loop to the example to restart if the answer is not satisfactory.
1. We add LangFuse to the example to track the usage of the nodes in the graph.
1. We add prompts management to the example to track the usage of the prompts in the graph.
1. We add user management to the example to track the usage of the users in the graph.
1. We add session management to the example to track the usage of the sessions in the graph.
1. We add retro from the users.


## Requirements

### Install the dependencies

```bash
uv sync
```

### Activate Virtual Environment

Before running any of the Python scripts, activate the virtual environment:

```bash
source .venv/bin/activate
```

### Install the LangFuse Docker Compose

```bash
git clone git@github.com:langfuse/langfuse.git
cd langfuse
docker-compose up
```

- Connect to the LangFuse UI at [http://localhost:3000](http://localhost:3000).
- Sign up for a new account.
- Create an organisation & a new project.

### Quick Setup: Environment Files

Now that LangFuse is running, you need to configure your environment variables for the workshop steps.

In the root of this project, you will find a `setup-envs.sh` script. This script will create the necessary `.env` files for you, but you will still need to populate them with the correct API keys.

```bash
./setup-envs.sh
```

### Environment Variables: What You Need

Here is a breakdown of the variables needed for each step:
> **Note:** For this workshop, the required keys will be provided to you, but this is the standard process for your own projects.

**For Steps 1-7 (Basic Agent Keys):**

You will need to manually fill the step 1-7 envs with the following content:

```
OPENAI_API_KEY="your_openai_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

**For Steps 3-7 (LangFuse Integration):**

You will need to fill in the following values in step 3-7:

- `LANGFUSE_PUBLIC_KEY` – Your LangFuse project's public API key.
- `LANGFUSE_SECRET_KEY` – Your LangFuse project's secret API key.
- `LANGFUSE_HOST` – The URL of your LangFuse instance (e.g., `http://localhost:3000` for local Docker).

**Where to get these keys:**
- **LangFuse Keys**: In your LangFuse project settings, under "API Keys".
- **OpenAI/Tavily Keys**: From their respective platform websites.

## References

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangFuse](https://github.com/langfuse/langfuse)
- [LangFuse Docs](https://langfuse.com/docs)
