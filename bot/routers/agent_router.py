# router.py

from fastapi import APIRouter, HTTPException
from loguru import logger
from bot.utils.schema import ChatRequest, ChatResponse
from bot.interactors.agent_graph import run_agent

router = APIRouter()

@router.post("/chat", response_model=ChatResponse, summary="Chat with agent", tags=["Agent"])
async def chat(request: ChatRequest):
    """
    Handle a POST request to chat with the agent.

    This endpoint takes a natural language query and routes it through the LangGraph-powered agent.
    Depending on the query type, it may:
    - Echo the message
    - Set a reminder
    - Use an LLM for answering general questions

    Args:
        request (ChatRequest): A request body containing the user's message.

    Returns:
        ChatResponse: The agent's response, either echo, LLM answer, or reminder confirmation.

    Raises:
        HTTPException: error code if any error occurs during agent execution.
    """
    try:
        logger.info(f"Received chat query: {request.message}")
        result = run_agent(request.message)
        logger.info(f"Agent response: {result}")
        return ChatResponse(response=result)
    except Exception as e:
        logger.exception("Unhandled exception in /chat endpoint")
        raise HTTPException(status_code=500, detail="Internal server error")
