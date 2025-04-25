"""
FastMCP Client Example

This example demonstrates how to use the standalone FastMCP client
to interact with a FastMCP server, calling tools, resources, and prompts.
"""

import asyncio
import logging
import sys
from mcpsock import WebSocketClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("client_example")

async def main():
    """Run the client example"""
    logger.info("Starting FastMCP client example...")
    
    # Configure server URL
    server_url = "ws://localhost:8765/ws"
    
    # Connect to the server
    async with WebSocketClient(server_url) as client:
        try:
            # First, let's discover what's available on the server
            await discover_capabilities(client)
            
            # Example of calling tools
            await call_tool_examples(client)
            
            # Example of accessing resources
            await access_resource_examples(client)
            
            # Example of using prompts
            await use_prompt_examples(client)
            
        except Exception as e:
            logger.error(f"Error in client example: {str(e)}")
            import traceback
            traceback.print_exc()

async def discover_capabilities(client: WebSocketClient):
    """Discover available tools, resources, and prompts on the server"""
    logger.info("Discovering server capabilities...")
    
    # List available tools
    tools = await client.list_tools()
    logger.info(f"Found {len(tools)} tools:")
    for tool in tools:
        logger.info(f"  - {tool.name}: {tool.description}")
    
    # List available resources
    resources = await client.list_resources()
    logger.info(f"Found {len(resources)} resources:")
    for resource in resources:
        logger.info(f"  - {resource.name}: {resource.description}")
    
    # List available prompts
    prompts = await client.list_prompts()
    logger.info(f"Found {len(prompts)} prompts:")
    for prompt in prompts:
        logger.info(f"  - {prompt.name}: {prompt.description}")

async def call_tool_examples(client: WebSocketClient):
    """Examples of calling different tools"""
    logger.info("Running tool examples...")
    
    # Example 1: Query data
    query_result = await client.call_tool("/tools/data/query_data", {
        "query": "sales data for Q1 2024"
    })
    logger.info(f"Data query result: {query_result}")
    
    # Example 2: Send a chat message
    message_result = await client.call_tool("/tools/chat/send_message", {
        "message": "Hello from the client example!",
        "channel": "general"
    })
    logger.info(f"Message result: {message_result}")

async def access_resource_examples(client: WebSocketClient):
    """Examples of accessing different resources"""
    logger.info("Running resource examples...")
    
    # Example 1: Get sample dataset as JSON
    json_data = await client.get_resource("/resources/data/sample_dataset", {
        "format": "json"
    })
    logger.info(f"Sample dataset (JSON): {json_data}")
    
    # Example 2: Get sample dataset as CSV
    csv_data = await client.get_resource("/resources/data/sample_dataset", {
        "format": "csv"
    })
    logger.info(f"Sample dataset (CSV): {csv_data}")
    
    # Example 3: Get list of available models
    models = await client.get_resource("/resources/models/list")
    logger.info(f"Available models: {models}")

async def use_prompt_examples(client: WebSocketClient):
    """Examples of using different prompts"""
    logger.info("Running prompt examples...")
    
    # Example 1: Generate text using a template
    generated_text = await client.call_prompt("/prompts/generate/text", {
        "template": "Write a short summary about {{topic}}.",
        "variables": {
            "topic": "FastMCP protocol"
        }
    })
    logger.info(f"Generated text: {generated_text}")
    
    # Example 2: Use chat completion
    chat_result = await client.call_prompt("/prompts/chat/complete", {
        "system": "You are a helpful assistant that specializes in APIs.",
        "messages": [
            {"role": "user", "content": "What are the benefits of using WebSockets for API communication?"}
        ]
    })
    logger.info(f"Chat completion result: {chat_result}")

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
