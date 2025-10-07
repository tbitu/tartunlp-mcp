#!/usr/bin/env python3
"""
TartuNLP MCP Server provides translation services through the University of Tartu's TartuNLP API.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)
from pydantic import BaseModel


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tartunlp-mcp-server")


class TranslationRequest(BaseModel):
    """Model for translation requests."""
    text: str
    source_lang: str
    target_lang: str
    model: Optional[str] = None


class TartuNLPClient:
    """Client for TartuNLP translation services."""
    
    def __init__(self):
        self.base_url = "https://api.tartunlp.ai/translation/v2"
        self.timeout = 30.0
        
    async def translate(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Translate text using the TartuNLP API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Use TartuNLP API v2 endpoint for translation
            url = self.base_url
            
            payload = {
                "text": text,
                "src": source_lang,
                "tgt": target_lang
            }
            
            if model:
                payload["domain"] = model
                
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Translation request failed: {e}")
                raise
    

    
    async def get_supported_languages(self) -> Dict[str, Any]:
        """Get supported language pairs from the TartuNLP API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Get API configuration that shows supported languages
                response = await client.get(self.base_url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to get supported languages: {e}")
                # Return fallback structure if API call fails
                return {
                    "error": f"Could not fetch supported languages: {str(e)}",
                    "message": "Please check TartuNLP API documentation for current language pairs"
                }


# Initialize TartuNLP client
tartunlp_client = TartuNLPClient()

# Create MCP server
server = Server("tartunlp-mcp-server")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Return list of available tools."""
    return [
        Tool(
            name="translate_text",
            description="Translate text between supported language pairs using TartuNLP",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to translate"
                    },
                    "source_lang": {
                        "type": "string", 
                        "description": "Source language code (e.g., 'et', 'en', 'ru')"
                    },
                    "target_lang": {
                        "type": "string",
                        "description": "Target language code (e.g., 'et', 'en', 'ru')"
                    },
                    "model": {
                        "type": "string",
                        "description": "Optional model/domain specification",
                        "default": None
                    }
                },
                "required": ["text", "source_lang", "target_lang"]
            }
        ),

        Tool(
            name="get_supported_languages",
            description="Get list of supported language pairs and available languages",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "translate_text":
            args = arguments or {}
            text = args.get("text", "")
            source_lang = args.get("source_lang", "")
            target_lang = args.get("target_lang", "")
            model = args.get("model")
            
            if not text or not source_lang or not target_lang:
                return [TextContent(
                    type="text",
                    text="Error: text, source_lang, and target_lang are required"
                )]
            
            result = await tartunlp_client.translate(text, source_lang, target_lang, model)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
            

        elif name == "get_supported_languages":
            result = await tartunlp_client.get_supported_languages()
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
            
        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool {name}"
            )]
            
    except Exception as e:
        logger.error(f"Tool call failed: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Main server entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="tartunlp-mcp-server",
                server_version="0.1.0",
                capabilities=ServerCapabilities(
                    tools={}
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())