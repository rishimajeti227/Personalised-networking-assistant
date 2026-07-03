from fastapi import APIRouter
from app.models.schemas import (
    ConversationRequest, ConversationResponse,
    EventInput, FactCheckRequest, FactCheckResponse,
    FeedbackRequest, FeedbackResponse, FeedbackLogResponse,
    HistoryResponse,
)
from app.services import (
    event_analyzer, fact_checker, feedback_logger,
    history_logger, topic_generator,
)

router = APIRouter()

# default candidate labels used when the user's interests don't cover a theme
_DEFAULT_THEMES = [
    "AI", "healthcare", "blockchain", "education", "sustainability",
    "robotics", "cybersecurity", "finance", "business", "technology",
]


@router.post("/analyze-event")
def analyze_event(data: EventInput):
    # extracts up to 3 relevant themes from a raw event description
    return {"topics": event_analyzer.extract_event_themes(data.description)}


@router.post("/fact-check", response_model=FactCheckResponse)
def fact_check_endpoint(data: FactCheckRequest):
    # looks up the query on Wikipedia (cache-first) and returns a short summary
    return FactCheckResponse(summary=fact_checker.fact_check(data.query))


@router.post("/generate-conversation", response_model=ConversationResponse)
def generate_conversation(data: ConversationRequest):
    # merge user's interests into the candidate set so the classifier considers them
    candidates = list(set(_DEFAULT_THEMES + data.interests))
    themes = event_analyzer.extract_event_themes(data.description, candidate_labels=candidates)

    # only keep themes that have a real Wikipedia entry (filters hallucinated labels)
    verified_themes = [t for t in themes if fact_checker.fact_check(t)]

    suggestions = topic_generator.generate_topics(verified_themes or themes, data.interests)

    history_logger.log_conversation({
        "description": data.description,
        "interests": data.interests,
        "topics": verified_themes,
        "suggestions": suggestions,
    })
    return ConversationResponse(topics=verified_themes, suggestions=suggestions)


@router.get("/history", response_model=HistoryResponse)
def get_history():
    # returns the 5 most recent sessions so the frontend history panel stays concise
    return HistoryResponse(history=history_logger.load_history()[-5:])


@router.post("/feedback", response_model=FeedbackResponse)
def post_feedback(data: FeedbackRequest):
    feedback_logger.log_feedback(data.suggestion, data.action)
    return FeedbackResponse(status="ok")


@router.get("/feedback-log", response_model=FeedbackLogResponse)
def get_feedback_log():
    # caps at 10 entries to keep the telemetry panel lightweight
    return FeedbackLogResponse(feedback=feedback_logger.get_feedback()[-10:])
