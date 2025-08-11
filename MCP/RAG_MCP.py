# import sys
# import os

# # Add the parent directory to Python path so we can import from utils
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, List
from utils.rag import EmbRag
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import asyncio

class SearchRequest(BaseModel):
    query: str
    DOCS: str
    FAISS: str

mcp=FastMCP("RAG-MCP")

@mcp.tool()
async def search_docs(req: SearchRequest) -> str:
    """Search the documents for the query"""
    obj = EmbRag(docs_path=req.DOCS, faiss_path=req.FAISS)
    answer = obj.queryDB(req.query)
    return answer

if __name__ == "__main__":
    # Default transport is stdio; use transport="http" or "sse" if needed
    mcp.run()  # e.g., run with: `python RAG_MCP.py` or `fastmcp run RAG_MCP.py`
