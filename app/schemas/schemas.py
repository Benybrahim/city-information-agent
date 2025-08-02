"""Pydantic models for the City Assistant API.

All models use Sphinx-style docstrings and type annotations.
"""

from pydantic import BaseModel, Field
from typing import Any


class ChatRequest(BaseModel):
    """
    Request body for chat endpoint.

    :param message: User's message to the assistant.
    """

    message: str = Field(description="User's message to the assistant.")


class FunctionCall(BaseModel):
    """
    Representation of a single function/tool call made by the agent.

    :param tool: Name of the tool being called.
    :param parameters: Parameters to be passed to the tool.
    """

    tool: str = Field(description="Name of the tool to call.")
    parameters: dict[str, Any] = Field(description="Tool call parameters.")


class ChatResponse(BaseModel):
    """
    Structured response from the assistant.

    :param thinking: The agent's internal reasoning as a string.
    :param function_calls: The list of tool calls invoked to generate the response.
    :param response: The final answer/message to the user.
    """

    thinking: str = Field(description="Agent's internal reasoning or plan.")
    function_calls: list[FunctionCall] = Field(
        description="List of tool calls invoked by the agent."
    )
    response: str = Field(description="Final message to return to the user.")


class CityInput(BaseModel):
    """
    Model for city name input to tools.

    :param city: The city name.
    """

    city: str = Field(description="City name to retrieve info about.")


class HandoffInfo(BaseModel):
    """
    Info for handoff between agents/subagents.

    :param subagent_name: The name of the subagent being delegated to.
    :param reason: The reason for the handoff.
    """

    subagent_name: str = Field(description="Name of the subagent being called.")
    reason: str = Field(description="Reason for the handoff.")
