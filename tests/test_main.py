from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_response_valid() -> None:
    """Test basic happy path with a simple city query."""
    req = {"message": "Tell me about Tokyo"}
    response = client.post("/chat", json=req)
    assert response.status_code == 200
    data = response.json()
    # Check schema keys
    assert "thinking" in data
    assert "function_calls" in data
    assert "response" in data
    # Check types
    assert isinstance(data["thinking"], str)
    assert isinstance(data["function_calls"], list)
    assert isinstance(data["response"], str)
    # Function calls are list of dicts
    for fc in data["function_calls"]:
        assert "tool" in fc
        assert "parameters" in fc


def test_chat_handles_followup() -> None:
    """Test follow-up chat/clarification is handled."""
    req = {"message": "Any romantic ideas for the evening in Paris?"}
    response = client.post("/chat", json=req)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["thinking"], str)
    assert isinstance(data["response"], str)
    assert isinstance(data["function_calls"], list)


def test_invalid_request_body() -> None:
    """Test error for completely missing 'message'."""
    req = {}
    response = client.post("/chat", json=req)
    assert response.status_code in (400, 422, 500)


def test_invalid_method() -> None:
    """Test error if using GET on POST endpoint."""
    response = client.get("/chat")
    assert response.status_code == 405
