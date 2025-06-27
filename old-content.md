


## Example Step 1: State Definition

- Uses TypedDict for state structure
- Implements Annotated with operator.add for list fields that need concatenation reducers

---

## Example Step 1: Graph Construction

- Follows standard pattern:
  define state → add nodes → add edges → compile
- Initializes StateGraph with appropriate schema

---

## Example Step 1: Command Usage

- Uses Command objects with type annotations
- Combines state updates with control flow

---

## Example Step 1: Configuration

- Implements ConfigSchema
- Accesses config parameters in nodes

---

## Example Step 1: Graph Visualization (bonus)

- Implements Mermaid diagram generation

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

## React Pattern

REAsoning & ACTing.

---

## Agent Node

---

## n8n Example

---

## Further

- Check for "Possible Exercise" in the code.
