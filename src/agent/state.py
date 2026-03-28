"""LangGraph agent state definition."""

from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State that flows through the agent graph.

    Attributes:
        messages: Accumulated conversation messages (LLM + tool calls).
        hasil_data: Final JSON result from scraping (set by tool).
    """

    messages: Annotated[list, add_messages]
    hasil_data: str
