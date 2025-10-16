"""Entry point for running the TartuNLP MCP server as a module."""

# For Smithery deployment, use: uv run dev or uv run playground
# This file is kept for compatibility but FastMCP servers 
# should be run using Smithery CLI commands

from .server import create_server

if __name__ == "__main__":
    # Create the server instance
    server = create_server()
    # FastMCP servers need to be run via Smithery CLI
    print("To run this server locally, use: uv run dev or uv run playground")
    print("See: https://smithery.ai/docs/build/deployments/python")