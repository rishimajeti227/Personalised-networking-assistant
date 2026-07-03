# shared pytest fixtures — TestClient wraps the FastAPI app for in-process HTTP
# requests so tests run without a live server
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
