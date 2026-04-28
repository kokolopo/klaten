"""LangGraph graph definition and compilation."""

import os
from functools import partial

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from src.agent.nodes import agent_node, should_continue, tool_node
from src.agent.state import AgentState
from src.agent.tools import ALL_TOOLS

# System prompt that guides the agent's behavior
SYSTEM_PROMPT = (
    "Kamu adalah AI agent yang bertugas mengambil data Target dan Realisasi "
    "Pendapatan Asli Daerah (PAD) dari dashboard etax Kabupaten Klaten.\n\n"
    "Langkah-langkah:\n"
    "1. Gunakan tool 'get_current_year' untuk mengetahui tahun saat ini.\n"
    "2. Gunakan tool 'scrape_pad_realisasi' untuk mengambil data dari URL "
    "yang diberikan user.\n"
    "3. Tampilkan hasilnya dalam format JSON yang rapi.\n\n"
    "Selalu gunakan tools yang tersedia. Jangan mengarang data."
)

# OpenRouter base URL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def build_graph(
    model_name: str = "anthropic/claude-haiku-4.5",
    temperature: float = 0,
) -> StateGraph:
    """Build and compile the LangGraph agent graph.

    Architecture:
        START -> agent -> (conditional) -> tools -> agent -> ... -> END

    Args:
        model_name: OpenRouter model identifier (e.g. google/gemini-2.0-flash-001,
                     openai/gpt-4o, anthropic/claude-3.5-sonnet).
        temperature: LLM temperature (0 for deterministic).

    Returns:
        Compiled StateGraph ready for invocation.
    """
    # Initialize LLM via OpenRouter (OpenAI-compatible API)
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/klaten-pad-agent",
            "X-Title": "PAD Data Scraper Agent",
        },
    )
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # Build the graph
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent", partial(agent_node, llm_with_tools=llm_with_tools))
    graph.add_node("tools", tool_node)

    # Set entry point
    graph.set_entry_point("agent")

    # Add conditional edge: agent -> tools or END
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )

    # Tools always route back to agent
    graph.add_edge("tools", "agent")

    return graph.compile()
