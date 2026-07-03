from pydantic import BaseModel
from typing import List


# request/response models — Pydantic validates incoming JSON automatically

class EventInput(BaseModel):
    description: str


class UserInterests(BaseModel):
    interests: List[str]


class ConversationRequest(BaseModel):
    description: str
    interests: List[str]


class ConversationResponse(BaseModel):
    topics: List[str]
    suggestions: List[str]


class FactCheckRequest(BaseModel):
    query: str


class FactCheckResponse(BaseModel):
    summary: str


class FeedbackRequest(BaseModel):
    suggestion: str
    action: str  # "like" or "dislike"


class FeedbackResponse(BaseModel):
    status: str


class FeedbackLogResponse(BaseModel):
    feedback: List[dict]


class HistoryResponse(BaseModel):
    history: List[dict]
