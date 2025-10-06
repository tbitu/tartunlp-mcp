#!/usr/bin/env python3
"""
TartoNLP MCP Server fállá jorgalanbálvalusaid Tarto universitehta TartoNLP APIs bokte.
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


# Heivet loggendieđuid
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tartunlp-mcp-server")


class TranslationRequest(BaseModel):
    """Jorgalan jearaldagaid málle."""
    text: str
    source_lang: str
    target_lang: str
    model: Optional[str] = None


class TartuNLPClient:
    """TartoNLP-jorgalanbálvalusaid klieanta."""
    
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
        """Jorgalit teavstta TartuNLP API: ain."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # TartuNLP API v2 terminologiija jorgaleapmái
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
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Áicca sisačálihuvvon teavstta giela."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}"
            
            payload = {"text": text}
            
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Language detection failed: {e}")
                raise
    
    async def get_supported_languages(self) -> Dict[str, Any]:
        """Hága dorjojuvvon giellabáraid TartoNLP API:s."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Gávnna API-dieđuid mat galget čájehit doarjojuvvon gielaid
                response = await client.get(self.base_url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to get supported languages: {e}")
                # Ruovttoluotta vuođđostruktuvrii, jos API-hálaldat meattáhusat
                return {
                    "error": f"Could not fetch supported languages: {str(e)}",
                    "message": "Please check TartuNLP API documentation for current language pairs"
                }


# Álggat TartoNLP klieantta
tartunlp_client = TartuNLPClient()

# Ráhkat MCP-bálvá
server = Server("tartunlp-mcp-server")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Čájet listu olamuttus reaidduin."""
    return [
        Tool(
            name="translate_text",
            description="Jorgalit teavstta dorjojuvvon gielaid gaskkas TartuNLP bokte",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Teaksta maid jorgalit"
                    },
                    "source_lang": {
                        "type": "string", 
                        "description": "Gáldogiela koda (omd., 'et', 'en', 'ru')"
                    },
                    "target_lang": {
                        "type": "string",
                        "description": "Ulbmilgiela koda (omd., 'et', 'en', 'ru')"
                    },
                    "model": {
                        "type": "string",
                        "description": "Eavttolaš modealla/domeana spesifikašuvdna",
                        "default": None
                    }
                },
                "required": ["text", "source_lang", "target_lang"]
            }
        ),
        Tool(
            name="detect_language",
            description="Fuobmá sisačálihuvvon teavstta giela TartuNLP bokte",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Teaksta maid analyseret vai gávdnat giela"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="get_supported_languages",
            description="Gávnna listtu doarjojuvvon giellabárain ja gávnna gielaid",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Reaiddut gohččot."""
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
            
        elif name == "detect_language":
            args = arguments or {}
            text = args.get("text", "")
            
            if not text:
                return [TextContent(
                    type="text", 
                    text="Error: text is required"
                )]
            
            result = await tartunlp_client.detect_language(text)
            
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
    """Server- guossoheaddji váldodoaimmahat."""
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