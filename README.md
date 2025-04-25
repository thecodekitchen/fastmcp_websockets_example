# FastMCP WebSockets Example

This project demonstrates how to use the `mcpsock` package to create WebSocket-based communication between clients and FastMCP servers, enabling real-time communication between web clients and FastMCP services.

## Overview

The FastMCP WebSockets Example showcases a complete implementation of the MCP (Model Context Protocol) over WebSockets using the `mcpsock` package. This implementation:

1. Uses FastAPI to create a WebSocket server endpoint
2. Implements a router-based FastMCP server with tools, resources, and prompts
3. Demonstrates bidirectional communication between clients and the server
4. Provides a clean, decorator-based API for defining MCP endpoints

## Components

### Server (`server.py`)

The server component:
- Creates a FastAPI application with a WebSocket endpoint
- Uses the `WebSocketServer` class from `mcpsock` to handle MCP protocol messages
- Implements tools, resources, and prompts using decorators
- Handles WebSocket connections and message routing
- Processes client requests and sends responses

### Client (`client.py`)

The client component:
- Uses the `WebSocketClient` class from `mcpsock` to connect to the server
- Demonstrates how to discover available capabilities (tools, resources, prompts)
- Shows how to call tools, access resources, and use prompts
- Handles responses from the server

## How It Works

1. The server creates a `WebSocketServer` instance and defines handlers using decorators:
   - `@router.tool()` for tool endpoints
   - `@router.resource()` for resource endpoints
   - `@router.prompt()` for prompt endpoints
   - `@router.initialize()` for connection initialization
   - `@router.fallback()` for handling unknown methods

2. When a client connects via WebSocket:
   - The client initializes the connection with the server
   - The client can discover available capabilities
   - The client can call tools, access resources, and use prompts
   - The server processes requests and sends responses

3. The `mcpsock` package handles all the protocol details, including:
   - Message serialization and deserialization
   - Request/response matching
   - Error handling
   - WebSocket connection management

## Use Cases

This WebSocket implementation is useful for:

- **Web Applications**: Integrate FastMCP capabilities into web frontends
- **Real-time Services**: Enable real-time AI-powered features in applications
- **Distributed Systems**: Connect remote clients to FastMCP servers across networks

## Running the Example

1. Start the server:
   ```bash
   pip install -r requirements.txt
   python server.py
   ```
   This will start the FastAPI server on port 8765.

2. Run the client in a separate terminal:
   ```bash
   python client.py
   ```
   The client will connect to the server, discover available capabilities, and demonstrate various interactions.

Or with uv:

1. Start the server:
   ```bash
   uv run server.py
   ```

2. Run the client in a separate terminal:
   ```bash
   uv run client.py
   ```

## Dependencies

This project uses the following dependencies:

- **mcpsock** (>=0.1.0): The WebSocket implementation of the MCP protocol
- **FastAPI** (>=0.110.0,<0.116.0): Web framework for building the WebSocket server
- **Uvicorn** (>=0.27.0,<0.35.0): ASGI server for running the FastAPI application
- **FastMCP** (>=2.2.0,<2.3.0): The FastMCP library for creating MCP servers and clients
- **Websockets** (>=12.0,<16.0): WebSocket implementation for Python
- **Starlette** (>=0.46.2): ASGI framework used by FastAPI

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

## About mcpsock

The `mcpsock` package is a standalone implementation of the MCP (Model Context Protocol) over WebSockets. It provides:

1. A server-side implementation (`WebSocketServer`) for handling MCP requests
2. A client-side implementation (`WebSocketClient`) for connecting to MCP servers
3. A clean, decorator-based API for defining MCP endpoints
4. Full support for the MCP protocol, including tools, resources, and prompts

The package is designed to be easy to use and integrate with existing FastAPI applications.

## License

This example is provided under the same license as FastMCP (Apache-2.0).