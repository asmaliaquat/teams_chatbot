from bot.services.llm import get_chain
from langchain_core.prompts import PromptTemplate

# Echo Agent
def echo_agent(message: str) -> str:
    """
    Simply echo back the content after removing 'say:' prefix.
    """
    prompt_str = """
        Your task is to echo back the useful content after removing irrelevant content.
        You MUST NOT add generation guidlelines in response. 

        Content: {message}
    """
    prompt = PromptTemplate(template=prompt_str)
    chain = get_chain(prompt)
    response = chain.invoke({"message": message}).content

    return response