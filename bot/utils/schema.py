
from pydantic import BaseModel
from langgraph.graph import  MessagesState


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class State(MessagesState):
    query: str
    classification_result: str
    result: str