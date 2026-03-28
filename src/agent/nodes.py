"""LangGraph graph nodes for the PAD agent."""

from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode

from src.agent.state import AgentState
from src.agent.tools import ALL_TOOLS

# Prebuilt node that executes tool calls from the LLM
tool_node = ToolNode(ALL_TOOLS)


def agent_node(state: AgentState, llm_with_tools) -> dict:
    """Invoke the LLM with the current message history.

    The LLM decides whether to call a tool or provide a final answer.

    Args:
        state: Current agent state with message history.
        llm_with_tools: LLM instance with tools bound.

    Returns:
        Updated state with the LLM's response message.
    """
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """Determine the next step based on the LLM's last response.

    Routes to 'tools' if the LLM made tool calls,
    or to 'end' if it provided a final answer.
    """
    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"

    return "end"
