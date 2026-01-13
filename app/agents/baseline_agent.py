from typing import TypedDict
from langgraph.graph import StateGraph, END
import json


class AgentState(TypedDict):
    input: str
    output: str


def respond(state: AgentState) -> AgentState:
    text = state["input"].lower()
    steps = []

    # Rule 1: Open Google
    if "open google" in text:
        steps.append({
            "action": "OPEN_BROWSER",
            "target": "https://www.google.com"
        })

    # Rule 2: Open Amazon
    if "open amazon" in text:
        steps.append({
            "action": "OPEN_BROWSER",
            "target": "https://www.amazon.com"
        })

    # Rule 3: Search
    if "search for" in text:
        query = text.split("search for")[-1].strip()
        steps.append({
            "action": "SEARCH",
            "query": query
        })

    return {
        "input": state["input"],
        "output": json.dumps({"steps": steps}, indent=2)
    }


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("respond", respond)
    graph.set_entry_point("respond")
    graph.add_edge("respond", END)

    return graph.compile()


agent = build_agent()
