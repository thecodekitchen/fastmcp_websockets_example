"""
FastAPI WebSocket Gateway for FastMCP

This implementation uses FastAPI to provide a WebSocket interface to a composed
system of FastMCP servers. It uses FastMCP's in-memory transport (FastMCPTransport)
for direct communication between WebSocket connections and the FastMCP server.
"""

import asyncio
import json
from typing import Set

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from fastmcp import FastMCP, Client
from fastmcp.client.transports import FastMCPTransport

# Create FastAPI app for WebSocket connections
app = FastAPI(title="FastMCP WebSocket Gateway")

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()

# Create a composed FastMCP server system
def create_composed_mcp_system():
    # Main MCP server
    main_server = FastMCP("Composed MCP System")
    
    # Data sub-server
    data_server = FastMCP("Data Services")
    
    @data_server.tool()
    async def query_data(query: str) -> dict:
        """Query data with the given parameters"""
        return {"result": f"Data for query: {query}"}
    
    # Chat sub-server
    chat_server = FastMCP("Chat Services")
    
    @chat_server.tool()
    async def send_message(message: str, channel: str) -> dict:
        """Send a message to a specific channel"""
        return {"status": "sent", "channel": channel, "message": message}
    
    # Mount sub-servers to the main server
    main_server.mount("/data", data_server)
    main_server.mount("/chat", chat_server)
    
    return main_server

# Create the composed MCP server (singleton)
mcp_server = create_composed_mcp_system()

# WebSocket endpoint for client connections
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    
    try:
        # Create a client with in-memory transport directly to the MCP server
        # This is the key part - we're using FastMCPTransport for direct in-memory connection
        transport = FastMCPTransport(mcp_server)
        client = Client(transport)
        
        # Connect the client to the server
        await client.connect()
        
        # Handle client-to-server messages
        async def forward_client_messages():
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)
                    
                    # Extract method and params from the WebSocket message
                    method = data.get("method")
                    params = data.get("params", {})
                    
                    if not method:
                        await websocket.send_json({"error": "No method specified"})
                        continue
                    
                    # Call the MCP server method via the client
                    response = await client.call_method(method, params)
                    
                    # Send the response back to the WebSocket client
                    await websocket.send_json(response)
            except Exception as e:
                print(f"Error in forward_client_messages: {str(e)}")
        
        # Handle server-to-client messages (notifications)
        async def handle_server_notifications():
            try:
                while websocket.client_state == WebSocketState.CONNECTED:
                    notification = await client.receive_notification()
                    if notification:
                        await websocket.send_json({
                            "type": "notification",
                            "data": notification
                        })
            except Exception as e:
                print(f"Error in handle_server_notifications: {str(e)}")
        
        # Start both tasks
        client_task = asyncio.create_task(forward_client_messages())
        server_task = asyncio.create_task(handle_server_notifications())
        
        # Wait for either task to complete
        done, pending = await asyncio.wait(
            [client_task, server_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel any pending tasks
        for task in pending:
            task.cancel()
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error in websocket_endpoint: {str(e)}")
    finally:
        # Clean up
        active_connections.remove(websocket)
        

@app.get("/")
async def get_root():
    """Simple endpoint to check if the server is running"""
    return {
        "status": "ok",
        "server": "FastMCP WebSocket Gateway",
        "active_connections": len(active_connections)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
