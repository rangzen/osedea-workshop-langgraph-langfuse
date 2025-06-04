import logging
import operator
import os
import random
import readline
from typing import Annotated, Literal

from dotenv import load_dotenv
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from typing_extensions import TypedDict

logging.basicConfig(level=logging.INFO)

load_dotenv()

# Constants (default values)
GRAPH_OSEDEA_FIND_PERCENT = 0.5
"""
50% chance to find a result in Osedea docs.
If set to 0, we will never return a result.
If set to 1, we will always return a result.
"""
GRAPH_WEB_MAX_RESULTS_AT_START = 1
"""
The maximum number of results to return from web search.
If the search returns no results, we will increase this value by 2 each time we search again.
"""
MODEL_NAME = "gpt-4o-mini"
"""The model to use for the LLM"""
MODEL_TEMPERATURE = 0.0
"""The temperature to use for the LLM"""
EXAMPLES = [
    (
        "Who is Carl from Osedea?",
        "will use Osedea docs, and a 1 in 2 chance to find a result",
    ),
    ("Who is Darth Vader according to Wikipedia?", "will normally use Wikipedia"),
    (
        "Is the best way to win a war is to never start it?",
        "will normally use web search",
    ),
    ("What is the capital of France?", "will normally use web search"),
    (
        "What will be the weather tomorrow in L.A.?",
        "will normally use web search and reach max steps or LLM calls",
    ),
]


# Initialize LLM
# We can create a new LLM instance for each node, but it is not necessary in this simple graph example.
llm = ChatOpenAI(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)


class ConfigSchema(TypedDict):
    """Config schema for the graph."""

    osedea_find_percent: float
    """The percentage of chance to find a result in Osedea docs"""


class State(TypedDict):
    """State of the graph. Will be passed to each node."""

    question: str
    """The original question to answer"""
    context: Annotated[list, operator.add]
    """The context to use for the answer"""
    answer: str
    """The answer to the question"""
    web_max_results: int
    """The maximum number of results to return from web search"""
    steps_history: Annotated[list[str], operator.add]
    """The steps made so far"""


def choose_tool(
    state: State,
) -> Command[Literal["search_osedea", "search_web", "search_wikipedia"]]:
    """Node to choose the tool to use based on the question"""
    logging.info(f"Choosing a tool for the question: {state['question']}")

    # Check "naively" if the question is about a specific topic that we can find in the question.
    # In a real-world scenario, you would use a more sophisticated method to determine the tool to use.
    if "wikipedia" in state["question"].lower():
        logging.info("Routing to Wikipedia search...")
        return Command(
            update={"steps_history": ["choose wikipedia"]},
            goto="search_wikipedia",
        )
    elif "osedea" in state["question"].lower():
        logging.info("Routing to Osedea search...")
        return Command(
            update={"steps_history": ["choose osedea"]},
            goto="search_osedea",
        )
    else:
        logging.info("Routing to web search...")
        return Command(
            update={"steps_history": ["choose web"]},
            goto="search_web",
        )


def search_osedea(state: State, config: RunnableConfig) -> dict:
    """
    Node to simulate a search in Osedea docs.

    1 chance out of 2 to return that there is no result.
    1 chance out of 2 to return a "result".
    """

    logging.info("Searching in Osedea docs...")

    # If find percent is 0, we will never return a result
    # If find percent is 1, we will always return a result
    r = random.random()
    if config["configurable"]["osedea_find_percent"] > r:
        logging.info("Result found in Osedea docs.")
        return {
            "steps_history": ["result from osedea"],
            "context": [
                '<Document href="https://osedea.com/docs/"/>\n'
                f"Regarding the question {state['question']}, Osedea will provide the best service since this subject is their specialty.\n"
                "If your question is about Carl, he is a great human being and a great developer.\n"
                "When he dreams, there is RAG systems everywhere.\n"
                "</Document>"
            ],
        }
    else:
        logging.info("No result found in Osedea docs.")
        return {
            "steps_history": ["no result from osedea"],
            "context": ["No result found in Osedea docs."],
        }


def search_web(state: State) -> dict:
    """Node to search in the web for the question"""
    logging.info("Searching in web...")

    tavily_search = TavilySearchResults(max_results=state["web_max_results"])
    search_docs = tavily_search.invoke(state["question"])

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    logging.info(
        f"Search results: {len(search_docs)} results found (max results: {state['web_max_results']})."
    )

    # Un comment to simulate a web search with no results and reach max steps or LLM calls.
    # return {"steps_history": ["result from web"]}
    return {"steps_history": ["result from web"], "context": [formatted_search_docs]}


def search_wikipedia(state: State) -> dict:
    """Node to search in Wikipedia for the question"""
    logging.info("Searching in Wikipedia...")

    search_docs = WikipediaLoader(query=state["question"], load_max_docs=2).load()

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    # Extract the page names for logging
    pages = [doc.metadata["source"].split("/")[-1] for doc in search_docs]
    logging.info(f"Pages from Wikipedia: {pages}")

    return {
        "steps_history": ["result from wikipedia"],
        "context": [formatted_search_docs],
    }


def generate_answer(state: State) -> dict:
    """Node to generate an answer using the context and the question"""

    logging.info("Generating answer...")

    context = state["context"]
    question = state["question"]

    # Template
    answer_template = """Answer the question {question} using this context: {context}. And only the data from the context. Do not add information."""
    answer_instructions = answer_template.format(question=question, context=context)

    answer = llm.invoke(
        [SystemMessage(content=answer_instructions)]
        + [HumanMessage(content="Answer the question.")]
    )

    return {
        "steps_history": ["generate answer"],
        "answer": answer,
    }


def closure(state: State) -> dict:
    """Node to stop the graph and return the answer"""
    logging.info("Ending the graph.")

    logging.info("Steps history: " + " -> ".join(state["steps_history"]))

    return {}


# Build the graph
builder = StateGraph(State, config_schema=ConfigSchema)

# Nodes
builder.add_node("choose_tool", choose_tool)
builder.add_node("search_osedea", search_osedea)
builder.add_node("search_web", search_web)
builder.add_node("search_wikipedia", search_wikipedia)
builder.add_node("generate_answer", generate_answer)
builder.add_node("closure", closure)

# Edges
# Possible Exercise: use Send to call every search_ nodes
builder.add_edge(START, "choose_tool")
builder.add_edge("search_osedea", "generate_answer")
builder.add_edge("search_wikipedia", "generate_answer")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("generate_answer", "closure")
builder.add_edge("closure", END)

# Compile the graph
# Possible Exercise: add a cache to the graph
graph = builder.compile()

# Generate the PNG byte data
png_data = graph.get_graph().draw_mermaid_png()

# Save the PNG data to a file in the same directory than this script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "langgraph_mermaid_graph.png")
with open(file_path, "wb") as f:
    f.write(png_data)


def run_graph(question):
    """Run the graph with a question"""

    # Initialize state
    initial_state = State(
        question=question,
        context=[],
        answer="",
        steps_history=[],
        llm_calls=0,
        web_max_results=GRAPH_WEB_MAX_RESULTS_AT_START,
    )

    # Config (read-only in langgraph!)
    config = {
        "osedea_find_percent": GRAPH_OSEDEA_FIND_PERCENT,
    }

    # Run the graph
    result_state = graph.invoke(initial_state, config)

    return result_state["answer"]


def complete(text, state):
    """Autocomplete function for the question input"""
    options = [example[0] for example in EXAMPLES]
    matches = [option for option in options if option.startswith(text)]
    if state < len(matches):
        return matches[state]
    else:
        return None


if __name__ == "__main__":
    print("Welcome to the Osedea Workshop on Agent demo!")
    print()
    print("Here are some examples of questions you can ask (autocomplete with tab):")
    for question, description in EXAMPLES:
        print(f"- {question} ({description})")
    print()

    readline.set_completer(complete)
    # To avoid completing only on the start of the last word
    readline.set_completer_delims("")
    # This is the default binding, not working well on MacOS and new Linux terminals.
    # readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("bind ^I rl_complete")
    question = input("What is your question? ")
    if not question:
        print("No question provided.")
        exit(0)

    logging.info("Running graph...")
    answer = run_graph(question)
    logging.info(f"Answer: {answer.content}")
    logging.info("Graph finished.")
