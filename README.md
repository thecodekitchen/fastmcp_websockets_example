# FastMCP WebSockets Example

This project demonstrates how to create a WebSocket gateway for FastMCP servers, enabling real-time communication between web clients and FastMCP services.

## Overview

The FastMCP WebSockets Example provides a bridge between WebSocket clients and FastMCP servers. This implementation:

1. Uses FastAPI to create a WebSocket server endpoint
2. Connects WebSocket clients to a composed FastMCP server system
3. Demonstrates bidirectional communication between clients and the FastMCP server
4. Leverages FastMCP's in-memory transport for efficient server-to-client communication

## Components

### Server (`server.py`)

The server component:
- Creates a FastAPI application with a WebSocket endpoint
- Implements a composed FastMCP server system with multiple sub-servers
- Handles WebSocket connections and message routing
- Translates between WebSocket messages and FastMCP method calls
- Manages client connections and notifications

### Client (`client.py`)

The client component:
- Connects to the WebSocket server using FastMCP's WSTransport
- Demonstrates how to call tools on the FastMCP server
- Shows how to handle responses from the server

## How It Works

1. The server creates a composed FastMCP system with multiple sub-servers (Data Services and Chat Services)
2. When a client connects via WebSocket, the server:
   - Creates a FastMCPTransport for direct in-memory communication with the FastMCP server
   - Establishes a Client connection using this transport
   - Sets up bidirectional message handling between the WebSocket and the FastMCP server
3. Client messages are parsed, routed to the appropriate FastMCP method, and responses are sent back
4. Server notifications are forwarded to the WebSocket client

## Use Cases

This WebSocket gateway pattern is useful for:

- **Web Applications**: Integrate FastMCP capabilities into web frontends
- **Real-time Services**: Enable real-time AI-powered features in applications
- **Distributed Systems**: Connect remote clients to FastMCP servers across networks
- **Cross-platform Integration**: Bridge between web clients and Python-based AI tools

## Running the Example

1. Start the server:
   ```
   python server.py
   ```
   This will start the FastAPI server on port 8765.

2. Run the client:
   ```
   python client.py
   ```
   The client will connect to the server, list available tools, and call example methods.

## Integration with FastMCP

This example demonstrates how FastMCP's flexible transport system can be extended to support WebSockets. The key components that make this possible:

1. **FastMCPTransport**: Used for direct in-memory communication between the WebSocket handler and the FastMCP server
2. **WSTransport**: Used by the client to connect to the WebSocket server

## Dependencies

This project uses the following dependencies with compatible version ranges:

- **FastAPI** (>=0.110.0,<0.116.0): Web framework for building the WebSocket server
- **Uvicorn** (>=0.27.0,<0.35.0): ASGI server for running the FastAPI application
- **FastMCP** (>=2.2.0,<2.3.0): The FastMCP library for creating MCP servers and clients
- **Websockets** (>=12.0,<16.0): WebSocket implementation for Python
- **Starlette** (>=0.31.0,<0.37.0): ASGI framework used by FastAPI

## Installation

We strongly recommend using [uv](https://github.com/astral-sh/uv) for package management, as it's significantly faster than pip and provides better dependency resolution. This is the same approach used by FastMCP.

This repository includes a `uv.lock` file to ensure consistent dependency resolution across different environments.

### Installing uv

If you don't have uv installed:

- **macOS**: `brew install uv`
- **Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

For more installation options, see the [uv documentation](https://github.com/astral-sh/uv).

### Setting Up Project
    
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/fastmcp-websockets-example.git
   cd fastmcp-websockets-example
   ```

2. Create a virtual environment:
   ```bash
   uv venv
   ```

3. Install the package and dependencies:
   ```bash
   uv pip install -e .
   ```

4. For development:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Alternative: Using pip

If you prefer using traditional pip:

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the package and dependencies:
   ```bash
   pip install -e .
   ```

3. For development:
   ```bash
   pip install -e ".[dev]"
   ```

## License

This example is provided under the same license as FastMCP (Apache-2.0).