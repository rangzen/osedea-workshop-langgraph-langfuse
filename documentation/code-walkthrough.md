# LangGraph & Langfuse Workshop: Code Walkthrough

This document serves as a comprehensive guide for conducting the workshop, providing detailed explanations and hands-on demonstrations for each step.

---

## Example Step 1: Overview

- Show the project structure overview
- Explain the progressive complexity approach (steps 1-7)
- Preview what we'll build: from linear workflow → agent with observability

- Show the diagram picture from step 1 and explain the workflow

---

## Example Step 1: State Definition

- TypedDict for state structure to provide type safety and IDE support
- Annotated with operator.add for list fields that need concatenation reducers
- State flows through all nodes, maintaining data continuity, save of this state, break and resume execution, etc.

---

## Example Step 1: Graph Construction

- Follows standard pattern:
  define state → add nodes → add edges → compile
- Initializes StateGraph with appropriate schema (e.g., run_graph)

---

## Example Step 1: Configuration

- Implements ConfigSchema
- Accesses config parameters in nodes (e.g., search_osedea)

---

## Example Step 1: Graph Visualization (bonus)

- Implements Mermaid diagram generation

---

## Example Step 1: Graph Execution

- Run with "Who is Darth Vader" (wikipedia search)
- Run with "Capital of France" (web search)
- Run with "Who is Carl" (osedea search with 50% chance of finding a result)
  - Show the logs
  - Show the steps history
  - Modify the GRAPH_OSEDEA_FIND_PERCENT to 0
  - Re-run with "Who is Carl" and outline the answer

If the answer is not found, the graph end with no result.

---

## Example Step 2: Diff with previous step

- Loop structure enables retry logic but requires safety controls
- New `check_answer_quality` node for evaluation
- Enhanced `choose_tool` with execution history awareness

- Show both graphs side by side

- Show the "Compare selected" view

- We need a steps max because now we have a loop in the graph
- We need a max call limit because we can call the LLM multiple times
- Choose tool now have some logic to decide which tool to use and use history
- We add a check_answer_quality node to evaluate the answer quality

---

## Example Step 2: Command

- Uses Command objects with type annotations (e.g., check_answer_quality)
- Combines state updates with control flow

---

## Example Step 3: Introduce Lanfuse

- Integrates Langfuse for enhanced logging and monitoring with mininal setup
- Captures user interactions and system responses
- Provides insights into model performance and user behavior

- Run main.py from step 3 and show the Langfuse dashboard
  - Tracing / Traces
    - The tree of the graph execution
    - The display of the nodes
    - Time and cost of each node

---

## Example Step 4: Prompt Management

Prompt management enables:
- versioning against regression issues
- A/B testing
- dynamic prompt selection

- Show "concise" and "kind" prompts in Langfuse
- Run "Best way to win a war" and show the diff between the two prompts
- Show the Langfuse dashboard with the two prompts
  - Traces with PromptTemplate
  - Prompts with Observations number and Metrics

---

## Example Step 5: Add User

We need to follow users: tracking, patterns, performance, personalization opportunities, etc.

- Show diff with previous step

---

## Example Step 6: Add Session

We need to follow sessions of users: conversation context, different memory usages: short term, long term, duration, etc.

- Show diff with previous step

---

## Example Step 7: User Feedback

We need to follow how the user reacts to the answer and the answer is determined by the prompts.
This is the equivalent of thumbs up / thumbs down in the answers of the chatbots, Copilot, etc.
It enables:
- data-driven prompt optimization, not "feelings-based" decisions
- automatization in prompt selection and optimization

- Show diff with previous step
- Show that the feedback is send after the graph execution
- Show the Langfuse dashboard with the feedback

---

## Building a good foundation

Build from the start with:

- observability of you graph execution, how much it costs, how long it takes, errors, etc.
- evals, to check the quality of the answers and optimize.
- good practices: type safety, error handling, configuration, etc.

Start simple, then add complexity step by step.

---

## The example : Improvements (1/2)

- Recursion limit can be better handled (see config)
- Limited error handling (e.g., no try/except blocks on external calls)
- Not a chatbot so no use of MessageState outside the preparation of the call to the LLM

Check also "Possible Exercise" in the code.

---

## The example : Improvements (2/2)

We still have a workflow:

- Orchestrator (choose_tool)
- Evaluator / Router (check_answer_quality)

Agent should react to environmental feedback and use our search_ nodes as tools.
This can be done with langgraph in 20 lines of code, instead of the example, but the goal is to show the pattern and step improvements.

---

## Going Further

Check for "Possible Exercise" in the code.

- Parallel searches
- Caching
- Token usage optimization
- Memory and context management

- Security
- Rate limiting
- Multi-agent orchestration

*This workshop provides a foundation for building production-ready AI systems. The journey from prototype to production requires careful attention to observability, error handling, and user experience. Continue exploring and building!*
