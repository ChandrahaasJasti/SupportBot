from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from pdb import set_trace

async def main():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["RAG_MCP.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            print("Connected to MCP server")

            # Get input from user
            text = input("Enter the query: ")
            query = {
                "query": text,
                "DOCS": "/home/chandrahaas/codes/Bot/DOCS",
                "FAISS": "/home/chandrahaas/codes/Bot/Faiss"
            }
            # Call the reverse_string tool
            result = await session.call_tool(
                "search_docs",
                arguments={"req": query}
            )

            # Print the result - accessing as object properties
            reversed_text = result.content[0].text

            print(f"MCP Response: {reversed_text}")

            print(50*"+", "DONE", 50*"+")
            print(dir(session))
            result = await session.list_tools()
            print("/n/n/n", result.tools)
            print(50*"+", "DONE", 50*"+")
            
            

if __name__ == "__main__":
    asyncio.run(main()) 