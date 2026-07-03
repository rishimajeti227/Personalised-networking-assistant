from unittest.mock import patch
from app.routers.conversation import router
import pytest


# AI-heavy endpoints are mocked to avoid loading DistilBERT and GPT-2 on every run


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_invalid_request_returns_422(client):
    # missing 'description' field triggers FastAPI's automatic Pydantic validation
    response = client.post("/generate-conversation", json={"interests": ["AI"]})
    assert response.status_code == 422


@patch("app.routers.conversation.event_analyzer.extract_event_themes")
def test_analyze_event(mock_extract, client):
    mock_extract.return_value = ["AI", "blockchain"]

    response = client.post("/analyze-event", json={"description": "Tech summit"})

    assert response.status_code == 200
    assert response.json()["topics"] == ["AI", "blockchain"]


@patch("app.routers.conversation.fact_checker.fact_check")
def test_fact_check_endpoint(mock_fact, client):
    mock_fact.return_value = "Blockchain is a distributed ledger technology."

    response = client.post("/fact-check", json={"query": "blockchain"})

    assert response.status_code == 200
    assert response.json()["summary"] == "Blockchain is a distributed ledger technology."


@patch("app.routers.conversation.history_logger.log_conversation")
@patch("app.routers.conversation.topic_generator.generate_topics")
@patch("app.routers.conversation.fact_checker.fact_check")
@patch("app.routers.conversation.event_analyzer.extract_event_themes")
def test_generate_conversation(mock_extract, mock_fact, mock_generate, mock_log, client):
    mock_extract.return_value = ["AI", "education"]
    # return a non-empty string so fact_check is truthy and verified_themes is populated
    mock_fact.return_value = "Some fact."
    mock_generate.return_value = [
        "Have you worked with any generative AI tools recently?",
        "What drew you to the education-tech space?",
    ]

    payload = {"description": "AI in Education summit", "interests": ["machine learning", "pedagogy"]}
    response = client.post("/generate-conversation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["topics"] == ["AI", "education"]
    assert len(data["suggestions"]) == 2
    mock_log.assert_called_once()


@patch("app.routers.conversation.history_logger.load_history")
def test_history_endpoint(mock_load, client):
    mock_load.return_value = [
        {"description": "AI summit", "topics": ["AI"], "timestamp": "2025-01-01T10:00:00"}
    ]

    response = client.get("/history")

    assert response.status_code == 200
    assert isinstance(response.json()["history"], list)


@patch("app.routers.conversation.history_logger.load_history")
def test_history_endpoint_empty(mock_load, client):
    mock_load.return_value = []

    response = client.get("/history")

    assert response.status_code == 200
    assert response.json()["history"] == []


@patch("app.routers.conversation.feedback_logger.log_feedback")
def test_feedback_endpoint_like(mock_log, client):
    payload = {"suggestion": "Have you tried any AI tools?", "action": "like"}
    response = client.post("/feedback", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_log.assert_called_once_with("Have you tried any AI tools?", "like")


@patch("app.routers.conversation.feedback_logger.log_feedback")
def test_feedback_endpoint_dislike(mock_log, client):
    payload = {"suggestion": "Tell me about blockchain.", "action": "dislike"}
    response = client.post("/feedback", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_log.assert_called_once_with("Tell me about blockchain.", "dislike")


@patch("app.routers.conversation.feedback_logger.get_feedback")
def test_feedback_log_endpoint(mock_get, client):
    mock_get.return_value = [
        {"suggestion": "Tell me about AI.", "feedback": "like", "timestamp": "2025-01-01T10:00:00"}
    ]

    response = client.get("/feedback-log")

    assert response.status_code == 200
    data = response.json()
    assert "feedback" in data
    assert data["feedback"][0]["feedback"] == "like"
