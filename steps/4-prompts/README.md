### Step 4: Prompts

From the LangFuse UI, create a new prompt with the following parameters:

- Name: `research-wikipedia-tavily-kind`
- Text Prompt: `You are kind.
You are a searcher that will use Wikipedia and Tavily search to answer the question: {{question}}, using this context: {{context}}.`
- Labels: check the `"Set the "production" label`

- Duplicate to `research-wikipedia-tavily-concise`.
- Change the promt text to `You are extremely concise. You answer with only one sentence. [...]`
