# bot/agent_graph.py

import re
from loguru import logger
from bot.utils.schema import State
from bot.services.llm import get_llm
from langgraph.graph import StateGraph, END, START
import os
import asyncio
from loguru import logger
from typing import Literal, Optional
from bot.utils.schema import State
from bot.services.llm import get_llm
from bot.utils.schema import ChatRequest
from langgraph.graph import StateGraph, END, MessagesState, START
from langgraph.checkpoint.sqlite import SqliteSaver
from bot.interactors.echo_agent import echo_agent
from bot.interactors.llm_agent import llm_agent
from bot.interactors.reminder_agent import reminder_agent





def classify_query(state):
    message = state["query"]
    """
    Use the LLM to classify user message into 'echo', 'reminder', or 'llm'.
    Falls back to simple heuristic if LLM call fails or returns invalid class.
    """
    prompt = f"""
Classify the following user query into one of these categories exactly: echo, reminder, or llm.
Return only the category name in lowercase.

Query: "{message}"
Category:"""

    try:
        llm = get_llm()
        response = llm.invoke(prompt)
        category = response.content.strip().lower()
        if category in {"echo", "reminder", "llm"}:
            return {"classification_result": category}
        else:
            logger.warning(f"LLM classifier returned invalid category '{category}', falling back to heuristic")
    except Exception as e:
        logger.error(f"LLM classification failed: {e}")

    # Fallback heuristic
    message_lower = message.lower()
    if message_lower.startswith("say:"):
        return "echo"
    elif "remind me" in message_lower and re.search(r"\d+\s*(minutes?|mins?)", message_lower):
        return "reminder"
    else:
        return "llm"




def echo_node(state: dict) -> dict:
    return {"result": echo_agent(state["query"])}

def reminder_node(state: dict) -> dict:
    return {"result": reminder_agent(state["query"])}

def llm_node(state: dict) -> dict:
    return {"result": llm_agent(state["query"])}

def end_node(state: dict) -> dict:
    return state




def graph_builder():
    workflow = StateGraph(State)

    workflow.add_node("classifyQuery", classify_query)
    workflow.add_node("echoNode", echo_node)
    workflow.add_node("reminderNode", reminder_node)
    workflow.add_node("llmNode", llm_node)

    workflow.add_edge(START, "classifyQuery")
    workflow.add_conditional_edges(
        "classifyQuery",
        lambda state: state["classification_result"],
        {
            "echo": "echoNode",
            "reminder": "reminderNode",
            "llm": "llmNode"
        }
    )
    workflow.add_edge("echoNode", END)
    workflow.add_edge("reminderNode", END)
    workflow.add_edge("llmNode", END)

    return workflow.compile()


agent_executor = graph_builder()


# API Handler for external use
def run_agent(message: str) -> str:
    """
    Main entry point to run the agent graph on a query string.
    """
    try:
        result = agent_executor.invoke({"query": message})
        return result.get("result", "No response.")
    except Exception as e:
        logger.exception("Failed to execute agent graph")
        return "Something went wrong running the agent."
