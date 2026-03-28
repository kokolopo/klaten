"""PAD Data Scraper Agent — CLI entry point."""

import asyncio
import sys

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

from src.agent.graph import SYSTEM_PROMPT, build_graph


async def run_agent(user_message: str | None = None) -> None:
    """Run the PAD scraper agent with the given user message.

    Args:
        user_message: Custom message to send to the agent.
                      Defaults to a standard PAD scraping request.
    """
    load_dotenv()

    if not user_message:
        user_message = (
            "Ambil data Target dan Realisasi PAD dari halaman "
            "https://dashboard.etax-klaten.id/monitoring_realisasi "
            "untuk tahun saat ini. Output dalam format JSON."
        )

    print("=" * 60)
    print("🤖 PAD Data Scraper Agent")
    print("=" * 60)
    print(f"\n📝 Request: {user_message}\n")
    print("⏳ Agent sedang bekerja...\n")

    # Build and invoke the graph
    graph = build_graph()

    initial_state = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ],
        "hasil_data": "",
    }

    # Stream events for visibility
    final_state = None
    async for event in graph.astream(initial_state):
        for node_name, node_output in event.items():
            if node_name == "agent":
                msg = node_output["messages"][-1]
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"🔧 Memanggil tool: {tc['name']}({tc['args']})")
                elif hasattr(msg, "content") and msg.content:
                    print(f"\n{'=' * 60}")
                    print("✅ Hasil Agent:")
                    print("=" * 60)
                    print(msg.content)

            elif node_name == "tools":
                for msg in node_output.get("messages", []):
                    if hasattr(msg, "content") and msg.content:
                        # Check if the tool returned JSON data
                        content = msg.content
                        if content.startswith("{"):
                            print(f"\n📊 Data berhasil diambil ({len(content)} chars)")
                        else:
                            print(f"📋 Tool result: {content}")

        final_state = event

    print(f"\n{'=' * 60}")
    print("🏁 Agent selesai.")
    print("=" * 60)


def main() -> None:
    """CLI entry point."""
    user_message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    asyncio.run(run_agent(user_message))


if __name__ == "__main__":
    main()
