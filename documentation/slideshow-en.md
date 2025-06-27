---
marp: true
author: "Cedric L'homme & Carl Lapierre"
size: 16:9
theme: gaia
footer: "All rights reserved © Osedea 2025"
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

:root {
  --color-background: #ffffff;
  --color-foreground: #1a0937;
  --color-highlight: #1a0937;
  --font-family: 'Inter', sans-serif;
  --font-family-heading: 'Inter', sans-serif;
}

section.lead {
  background-color: #1a0937;
}

section.lead h1 {
  color: #925cff;
  text-align: left;
}

section.lead p {
  color: white;
  text-align: left;
}

.container {
  display: flex;
  gap: 2rem;
  align-items: center;
}
.col {
  flex: 1;
}
.col-center {
  display: flex;
  justify-content: center;
}
</style>

<!-- _class: lead -->

# Osedea Workshop on LangGraph and Langfuse

Event oriented programming or microservices are too easy to debug? You want randomness in your results?

You have it with agents!

---

## Goal of this workshop

Look into a simple agentic workflow built with LangGraph & introduce observability with Langfuse.

*Beware, this content will probably be outdated in 6 months...*

---

## What are Agents?

Agents are systems that use a Large Language Model (LLM) to **reason** through a problem, create a **plan**, and execute a sequence of **actions** to accomplish a **goal autonomously**. They can use **tools**, like search engines or code interpreters, to find information and perform tasks.

---

## A Simple Agentic Workflow

<div class="container">
<div class="col">
A basic agent follows a linear path from input to output. At it's core an agent will make a decision based on the context it has.
</div>
<div class="col col-center">

![width:230px](./assets/agent.png)

</div>
</div>

---
## Improving Model Behaviour

![width:970px](./assets/agent-behaviour.png)

---

## The ReAct Pattern

<div class="container">
<div class="col">
ReAct (Reason + Act) is a common agentic pattern. Instead of a single decision, the agent loops through  a process of reasoning and acting until it reaches a final answer.
</div>
<div class="col col-center">

![width:400px](./assets/react.png)

</div>
</div>

---

## What is LangGraph?

LangGraph is a library from the LangChain team for building stateful, multi-agent applications. It allows you to define agent workflows as graphs, where nodes represent functions (or LLM calls) and edges represent the control flow between them.

This graph-based approach is particularly well-suited for creating the cyclical and complex logic required by agentic systems.

---

## LangGraph

Control flow (edges) and state updates (nodes).

![width:800px](https://langchain-ai.github.io/langgraph/concepts/img/agent_workflow.png)

---

## LangGraph Core Concepts

*   **State:** A central, persistent object that is passed between all nodes in the graph. Each node can update the state.
*   **Interruptions:** The graph can be paused at any point, for example, to wait for human input or to handle an error. This is essential for human-in-the-loop workflows.
*   **Checkpoints:** LangGraph can automatically save the state of the graph. This allows you to resume long-running tasks, recover from failures, and inspect the full history of an agent's work.

---

## LangGraph: Instrumented For Observability

A key advantage of using a framework like LangGraph is its built-in instrumentation. The framework is designed to emit telemetry data out-of-the-box.

By simply adding a callback handler from a tool like Langfuse, you can capture detailed traces of your agent's execution, making complex workflows easy to observe, debug, and optimize.

---

## What is Langfuse?

Langfuse is an open-source observability and analytics platform specifically designed for LLM applications. It helps you:

- **Trace** complex chains and agentic systems.
- **Debug** errors and unexpected outputs.
- **Evaluate** the quality and performance of your application.
- **Manage** prompts and versions.

---

## References & Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Langfuse Documentation](https://langfuse.com/docs)
- [Langfuse & LangGraph Integration Cookbook](https://langfuse.com/docs/integrations/langchain/example-python-langgraph)
