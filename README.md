# Workshop on LangGraph & LangFuse

Going from the [Osedea Hackaton Boilerplate](https://github.com/rangzen/osedea-hackaton-2025-boilerplate) LangGraph example (~almost) to a LangFuse integrated example.

Steps:

1. The initial example is a LangGraph example that uses Wikipedia and Tavily as nodes in the graph.
1. We add LangFuse to the example to track the usage of the nodes in the graph.
1. We add prompts management to the example to track the usage of the prompts in the graph.
1. We add user management to the example to track the usage of the users in the graph.
1. We add session management to the example to track the usage of the sessions in the graph.
1. We add retro from the users.

## Notes

We are using Wikipedia and Tavily as nodes in the graph, not as tools for an agent.

## Requirements

### Install the dependencies

```bash
uv sync
```

### Install the LangFuse Docker Compose

```bash
git clone git@github.com:langfuse/langfuse.git
cd langfuse
docker-compose up
```

- Connect to the LangFuse UI at [http://localhost:3000](http://localhost:3000).
- Sign up for a new account.
- Create an organisation, a new project and create API keys.
- In each directory, create `.env` files from the `.env.example` files with the API keys.

### Step Prompt

From the LangFuse UI, create a new prompt with the following parameters:

- Name: `research-wikipedia-tavily-kind`
- Text Prompt: `You are kind.
You are a searcher that will use Wikipedia and Tavily search to answer the question: {{question}}, using this context: {{context}}.`
- Labels: check the `"Set the "production" label`

- Duplicate to `research-wikipedia-tavily-concise`.
- Change the promt text to `You are concise. [...]`

### Step User

- Try with random user IDs, see [main.py](./steps/4-users/main.py#L387) for the user ID generation.
- Try with the same user ID, see [main.py](./steps/4-users/main.py#L389) for a fixed user ID.

### Step Session

- Try with random session IDs, see [main.py](./steps/5-sessions/main.py#L392) for the session ID generation.

## References

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangFuse](https://github.com/langfuse/langfuse)
- [LangFuse Docs](https://langfuse.com/docs)
