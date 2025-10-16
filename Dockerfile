# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy pyproject.toml first for better layer caching
COPY pyproject.toml ./

# Install the package and dependencies
RUN pip install --no-cache-dir -e .

# Copy the source code
COPY tartunlp_mcp_server/ ./tartunlp_mcp_server/

# Set the entrypoint to run the MCP server via stdio
ENTRYPOINT ["python", "-m", "tartunlp_mcp_server"]
