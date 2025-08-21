import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# ---- Agent State ----
class DemoState(BaseModel):
    messages: List[Any] = []
    last_mcp_response: Optional[Dict[str, Any]] = None
    error_log: List[str] = []


# ---- MCP Tool Wrapper ----
@tool
async def query_mcp_server(query: str) -> Dict[str, Any]:
    """
    Simulates invoking a demo MCP server.
    Replace this stub with real MCP client call logic.
    """
    try:
        # For demo, we just echo back structured response
        return {"mcp_response": f"Demo MCP server received query: {query}"}
    except Exception as e:
        return {"error": str(e)}


# ---- Workflow Graph ----
def build_graph():
    graph = StateGraph(DemoState)

    # ToolNode from LangGraph wraps tools
    mcp_node = ToolNode([query_mcp_server])
    graph.add_node("mcp_tool", mcp_node)

    # The input node simply routes message to MCP tool
    def user_input_node(state: DemoState):
        if state.messages:
            last = state.messages[-1].content
            return {"query_mcp_server": last}
        return {}

    graph.add_node("user_input", user_input_node)

    # Edges
    graph.add_edge("user_input", "mcp_tool")
    graph.add_edge("mcp_tool", "user_input")

    # Entry point
    graph.set_entry_point("user_input")
    return graph


# ---- Execution Harness ----
async def run_agent():
    graph = build_graph().compile()
    state = DemoState(messages=[HumanMessage(content="hello mcp")])
    async for s in graph.astream(state, limit=3):
        print("State update:", s)


if __name__ == "__main__":
    asyncio.run(run_agent())