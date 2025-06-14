import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_summarize_text():
    test_text = "This is a test text. It contains multiple sentences. We want to test if the summarization works correctly. The summary should be shorter than the original text."
    response = client.post(
        "/summarize",
        json={"text": test_text, "num_sentences": 2}
    )
    assert response.status_code == 200
    assert "summary" in response.json()
    assert len(response.json()["summary"].split(". ")) <= 2

def test_summarize_empty_text():
    response = client.post(
        "/summarize",
        json={"text": "", "num_sentences": 2}
    )
    assert response.status_code == 400
    assert "Text cannot be empty" in response.json()["detail"]

def test_summarize_short_text():
    response = client.post(
        "/summarize",
        json={"text": "Too short", "num_sentences": 2}
    )
    assert response.status_code == 400
    assert "Text must contain at least 10 words" in response.json()["detail"]

def test_summarize_invalid_sentences():
    response = client.post(
        "/summarize",
        json={"text": "This is a test text with more than ten words to test the validation of the number of sentences parameter.", "num_sentences": 0}
    )
    assert response.status_code == 400
    assert "Number of sentences must be at least 1" in response.json()["detail"] 