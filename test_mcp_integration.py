import pytest
import asyncio
from langchain_core.messages import HumanMessage
from run_demo import build_graph, DemoState

@pytest.mark.asyncio
async def test_mcp_integration_echo():
    graph = build_graph().compile()

    # Initial state with user query
    state = DemoState(messages=[HumanMessage(content="test query")])

    responses = []
    async for s in graph.astream(state, limit=2):
        responses.append(s)

    # After execution, responses should contain an MCP server reply
    found = any("mcp_response" in str(s) for s in responses)
    assert found, "Expected MCP response in graph state"

    # Ensure no errors logged
    for s in responses:
        assert "error" not in str(s).lower()