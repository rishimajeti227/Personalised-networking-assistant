# all network calls are mocked so tests are fast, deterministic, and CI-safe
from unittest.mock import MagicMock, patch
from app.services.fact_checker import fact_check


@patch("app.services.fact_checker.requests.get")
def test_fact_check_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"extract": "FastAPI is a modern web framework."}
    mock_get.return_value = mock_response

    result = fact_check("FastAPI")

    assert result == "FastAPI is a modern web framework."


@patch("app.services.fact_checker.requests.get")
def test_fact_check_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = fact_check("UnknownTermXYZ")

    assert "lookup yielded no match" in result


@patch("app.services.fact_checker.requests.get")
def test_fact_check_network_exception(mock_get):
    # uses a topic not in the pre-seeded cache so the mock is actually invoked
    mock_get.side_effect = Exception("Connection timeout")

    result = fact_check("quantumcomputing")

    assert "network error" in result.lower()


@patch("app.services.fact_checker.requests.get")
def test_fact_check_missing_extract_key(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}  # no 'extract' key
    mock_get.return_value = mock_response

    result = fact_check("SomeTopic")

    assert result == "No summary found."
