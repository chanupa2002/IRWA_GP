# test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # adjust if your FastAPI file is named differently

client = TestClient(app)


def test_health():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_success(monkeypatch):
    """Test the search endpoint with mocked dependencies"""

    # Mock normalize_and_tokenize
    def mock_normalize_and_tokenize(query: str):
        return ["ai", "research"]

    # Mock search_semantic_scholar
    def mock_search_semantic_scholar(query: str, limit: int = 20):
        return [
            {
                "title": "Artificial Intelligence Research",
                "authors": ["John Doe", "Jane Smith"],
                "year": 2024,
                "url": "https://example.com/paper1",
                "pdfUrl": "https://example.com/paper1.pdf",
                "source": "Semantic Scholar",
                "abstract": "This is a mock abstract about AI research.",
            }
        ]

    monkeypatch.setattr("app.main.normalize_and_tokenize", mock_normalize_and_tokenize)
    monkeypatch.setattr("app.main.search_semantic_scholar", mock_search_semantic_scholar)

    response = client.get("/search?query=AI research")
    assert response.status_code == 200
    data = response.json()
    assert "papers" in data
    assert isinstance(data["papers"], list)
    assert data["papers"][0]["title"] == "Artificial Intelligence Research"

    print(data)

def test_search_invalid(monkeypatch):
    """Test when normalize_and_tokenize raises an error"""

    def mock_normalize_and_tokenize(query: str):
        raise ValueError("NLP error")

    monkeypatch.setattr("app.main.normalize_and_tokenize", mock_normalize_and_tokenize)

    response = client.get("/search?query=test")
    assert response.status_code == 500
    assert response.json()["detail"] == "NLP processing failed."
