#!/usr/bin/env python3
"""
TartuNLP MCP Server provides translation services through the University of Tartu's TartuNLP API.
"""

import json
import logging
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field
from smithery.decorators import smithery

# Configuration schema for Smithery MCP
class ServerConfig(BaseModel):
    """Configuration schema for TartuNLP MCP Server."""
    timeout: int = Field(
        default=5000,
        description="Request timeout in milliseconds",
        ge=1000,
        le=30000
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TartuNLP")


class TartuNLPClient:
    """Client for TartuNLP translation services."""
    def __init__(self, timeout: int = 5000):
        self.base_url = "https://api.tartunlp.ai/translation/v2"
        self.timeout = timeout / 1000.0  # Convert ms to seconds
        
    async def translate(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Translate text using the TartuNLP API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
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
                response = await client.get(self.base_url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to get supported languages: {e}")
                return {
                    "error": f"Could not fetch supported languages: {str(e)}",
                    "message": "Please check TartuNLP API documentation for current language pairs"
                }


@smithery.server(config_schema=ServerConfig)
def create_server(config: ServerConfig = None):
    """Create and configure the TartuNLP MCP server for Smithery deployment."""
    # Use default config if none provided
    if config is None:
        config = ServerConfig()
    
    # Initialize the client with the provided config
    client = TartuNLPClient(timeout=config.timeout)
    
    logger.info(f"TartuNLP MCP server initialized with timeout={config.timeout}ms")
    
    # Create FastMCP server
    server = FastMCP(name="TartuNLP")
    
    @server.tool()
    async def translate_text(
        text: str,
        source_lang: str,
        target_lang: str,
        model: Optional[str] = None,
        ctx: Context = None
    ) -> str:
        """Translate text between supported language pairs using TartuNLP.
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'et', 'en', 'ru')
            target_lang: Target language code (e.g., 'et', 'en', 'ru')
            model: Optional model/domain specification
        """
        try:
            result = await client.translate(text, source_lang, target_lang, model)
            return json.dumps(result, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    @server.tool()
    async def get_supported_languages(ctx: Context = None) -> str:
        """Get list of supported language pairs and available languages."""
        try:
            result = await client.get_supported_languages()
            return json.dumps(result, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to get languages: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    return server