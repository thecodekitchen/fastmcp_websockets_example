"""
FastMCP WebSocket Router Example

This example demonstrates how to use the DecoratorRouter to create
a FastMCP server that supports tools, resources, and prompts.
"""

import uvicorn
from fastapi import FastAPI, WebSocket
import logging
from mcpsock import WebSocketServer
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="FastMCP WebSocket Router Example")

# Create router with decorators
router = WebSocketServer()

@router.initialize()
async def handle_initialize(message: Dict[str, Any], websocket: WebSocket):
    """Initialize the FastMCP connection"""
    protocol_version = message.get("params", {}).get("protocolVersion", "2.0")
    return {
        "protocolVersion": protocol_version,
        "capabilities": {
            "sampling": {},
            "resources": {},
            "prompts": {}
        },
        "roots": {"listChanged": True}
    }

#
# Tool Handlers
#

@router.tool("/tools/data/query_data")
async def query_data(message: Dict[str, Any], websocket: WebSocket):
    """Query data from the system using a specified query string"""
    params = message.get("params", {})
    query = params.get("query", "")
    logger.info(f"Querying data with: {query}")
    return {"result": f"Data for query: {query}", "timestamp": "2024-04-24T12:34:56Z"}

@router.tool("/tools/chat/send_message")
async def send_message(message: Dict[str, Any], websocket: WebSocket):
    """Send a message to a specific channel"""
    params = message.get("params", {})
    msg = params.get("message", "")
    channel = params.get("channel", "")
    logger.info(f"Sending message to {channel}: {msg}")
    return {"status": "sent", "channel": channel, "message": msg, "timestamp": "2024-04-24T12:34:56Z"}

#
# Resource Handlers
#

@router.resource("/resources/data/sample_dataset")
async def get_sample_dataset(message: Dict[str, Any], websocket: WebSocket):
    """Provides access to a sample dataset in various formats"""
    params = message.get("params", {})
    format_type = params.get("format", "json")
    
    logger.info(f"Getting sample dataset in format: {format_type}")
    
    # Here we'd typically fetch data from a database or file
    # For this example, we'll just return some sample data
    if format_type == "json":
        return {
            "id": "sample-dataset-001",
            "data": [
                {"id": 1, "name": "Item 1", "value": 10.5},
                {"id": 2, "name": "Item 2", "value": 20.8},
                {"id": 3, "name": "Item 3", "value": 15.2}
            ],
            "metadata": {
                "description": "Sample dataset for testing",
                "created": "2024-04-24T12:00:00Z"
            }
        }
    elif format_type == "csv":
        return "id,name,value\n1,Item 1,10.5\n2,Item 2,20.8\n3,Item 3,15.2"
    else:
        raise ValueError(f"Unsupported format: {format_type}")

@router.resource("/resources/models/list")
async def list_models(message: Dict[str, Any], websocket: WebSocket):
    """Returns a list of available models"""
    logger.info("Listing available models")
    
    return {
        "models": [
            {
                "id": "model-base",
                "name": "Base Model",
                "description": "General purpose language model"
            },
            {
                "id": "model-code",
                "name": "Code Model",
                "description": "Specialized for code generation and understanding"
            },
            {
                "id": "model-science",
                "name": "Science Model",
                "description": "Optimized for scientific and technical content"
            }
        ]
    }

#
# Prompt Handlers
#

@router.prompt("/prompts/generate/text")
async def generate_text(message: Dict[str, Any], websocket: WebSocket):
    """Generates text based on a template and variables"""
    params = message.get("params", {})
    template = params.get("template", "")
    variables = params.get("variables", {})
    
    logger.info(f"Generating text with template: {template}")
    logger.debug(f"Variables: {variables}")
    
    # Simple template rendering
    result = template
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        result = result.replace(placeholder, str(value))
    
    return result

@router.prompt("/prompts/chat/complete")
async def chat_completion(message: Dict[str, Any], websocket: WebSocket):
    """Simulates a chat completion endpoint"""
    params = message.get("params", {})
    messages = params.get("messages", [])
    system_prompt = params.get("system", "You are a helpful assistant.")
    
    logger.info(f"Chat completion with {len(messages)} messages")
    logger.debug(f"System prompt: {system_prompt}")
    
    # In a real implementation, this would call an actual LLM
    # For this example, we'll just echo back the last message
    if messages:
        last_message = messages[-1].get("content", "")
        return f"You said: {last_message}\n\nThis is a simulated response. In a real implementation, this would be generated by a language model."
    else:
        return "No messages provided. Please include at least one message."

@router.fallback()
async def handle_unknown(message: Dict[str, Any], websocket: WebSocket):
    """Handle unknown methods"""
    method = message.get("method", "")
    raise ValueError(f"Unknown method: {method}")

# Attach router to app
router.attach_to_app(app)

# Run the app
if __name__ == "__main__":
    logger.info("Starting FastMCP WebSocket Router Example...")
    uvicorn.run(app, host="0.0.0.0", port=8765)
