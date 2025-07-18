from bot.services.llm import get_llm
from loguru import logger
# LLM Agent - handles free text queries
def llm_agent(message: str) -> str:
    try:
        llm = get_llm()
        return (llm.invoke(message)).content
    except Exception as e:
        logger.exception("LLM agent failed")
        return "LLM failed to respond."