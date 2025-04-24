"""
FastMCP WebSocket Client

This client connects to a FastMCP WebSocket Gateway using FastMCP's
built-in WSTransport and interacts with the composed MCP server system.
"""

from fastmcp import Client
from fastmcp.client.transports import WSTransport
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Connect to our WebSocket endpoint
transport = WSTransport("ws://localhost:8765/ws")  # The endpoint we defined in our gateway
client = Client(transport)

async def main():
    print("Starting client...")
    async with client:
        print(f"Client connected: {client.is_connected()}")
        
        # Add a small delay to ensure connection is established
        await asyncio.sleep(1)
        
        try:
            # List all available tools
            print("Listing tools...")
            tools = await client.list_tools()
            print(f"Available tools: {tools}")
            
            # Call the data server's query_data tool
            if any(tool.name == "/data/query_data" for tool in tools):
                print("Calling data query tool...")
                result = await client.call_tool("/data/query_data", {"query": "example query"})
                print(f"Data query result: {result}")
            else:
                print("The data query tool was not found.")
            
            # Call the chat server's send_message tool
            if any(tool.name == "/chat/send_message" for tool in tools):
                print("Calling chat message tool...")
                result = await client.call_tool("/chat/send_message", {
                    "message": "Hello from WebSocket client!",
                    "channel": "general"
                })
                print(f"Chat message result: {result}")
            else:
                print("The chat message tool was not found.")
            
            # Keep the connection alive for a moment
            print("Waiting for 5 seconds to ensure all responses are received...")
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"Error during client operations: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
