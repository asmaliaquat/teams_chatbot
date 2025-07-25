import os
# from langchain.chat_models import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI


# Initialize LLM (you can parameterize model name, temperature later)
mistral_api_key  = os.getenv("MISTRAL_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_llm():
    
    if openai_api_key:
        llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
        
    else :
        llm = ChatMistralAI(
            model="mistral-small-2503", api_key=mistral_api_key)
        
# Initialize LLM (you can parameterize model name, temperature later)
mistral_api_key  = os.getenv("MISTRAL_API_KEY")
def get_llm():
    llm = ChatMistralAI(
        model="mistral-small-2503", api_key=mistral_api_key)
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    return llm

def get_chain(prompt, parser=None, setup=None):
    try:
        llm = get_llm()
        if parser:
            chain = prompt | llm | parser
        elif setup:
            chain = setup | prompt | llm
        else:
            chain = prompt | llm
        return chain
    except Exception as e:
        raise Exception(f"Error creating chain: {e}")