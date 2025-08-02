from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient

from app.main import app

client: TestClient = TestClient(app)


@pytest.fixture(autouse=True)
def patch_agent(monkeypatch: pytest.MonkeyPatch) -> Callable[..., None]:
    """
    Auto-mock Runner.run for all tests to prevent real OpenAI/Agent calls.

    :param monkeypatch: Pytest's monkeypatch fixture.
    :return: A function for test-scoped patching (not used here, but can extend).
    """

    class DummyResult:
        final_output: str = (
            '{"thinking":"Mocked thinking",'
            '"function_calls":[{"tool":"city_facts_tool","parameters":{"city":"Tokyo"}}],'
            '"response":"Mocked response"}'
        )

    async def dummy_run(agent: object, message: str, session: object = None) -> DummyResult:
        return DummyResult()

    import app.main

    app.main.Runner.run = dummy_run

    def restore_patch() -> None:
        pass

    return restore_patch


def test_chat_response_valid() -> None:
    req: dict[str, str] = {"message": "Tell me about Tokyo"}
    response = client.post("/chat", json=req)
    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert "thinking" in data
    assert "function_calls" in data
    assert "response" in data
    assert isinstance(data["thinking"], str)
    assert isinstance(data["function_calls"], list)
    assert isinstance(data["response"], str)
    for fc in data["function_calls"]:
        assert isinstance(fc, dict)
        assert "tool" in fc
        assert "parameters" in fc


def test_chat_handles_followup() -> None:
    req: dict[str, str] = {"message": "Any romantic ideas for the evening in Paris?"}
    response = client.post("/chat", json=req)
    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert isinstance(data["thinking"], str)
    assert isinstance(data["function_calls"], list)
    assert isinstance(data["response"], str)
