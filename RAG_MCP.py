from typing import Any, Dict, List

from fastmcp import FastMCP, Context


# Create a FastMCP server instance
mcp = FastMCP(name="RAG_MCP_Server")


@mcp.tool
def echo(message: str) -> str:
    """Echo a message back to the caller."""
    return message


@mcp.tool
async def health(ctx: Context) -> str:
    """Health check tool; returns 'ok' and logs to the client."""
    await ctx.info("Health check requested")
    return "ok"


@mcp.tool
async def search_docs(query: str, top_k: int = 5) -> Dict[str, Any]:
    """Search your RAG index for relevant chunks. Placeholder implementation.

    Args:
        query: Natural language query to search.
        top_k: Maximum number of results to return.

    Returns:
        A dictionary with the query and an empty results list.
    """
    # Placeholder: wire this to your FAISS/RAG pipeline later
    return {"query": query, "results": [], "top_k": top_k}


@mcp.resource("config://version")
def get_version() -> str:
    """Return the server version string."""
    return "0.1.0"


@mcp.prompt
def summarize_request(text: str) -> str:
    """Return a simple summarization prompt for the provided text."""
    return f"Please summarize the following text in 3-5 bullet points:\n\n{text}"


if __name__ == "__main__":
    # Default transport is stdio; use transport="http" or "sse" if needed
    mcp.run()  # e.g., run with: `python RAG_MCP.py` or `fastmcp run RAG_MCP.py`
