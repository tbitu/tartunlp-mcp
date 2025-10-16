# TartuNLP MCP Server

[![Docker](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/tbitu/tartunlp-mcp/pkgs/container/tartunlp-mcp)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Model Context Protocol (MCP) server that provides seamless access to [TartuNLP translation services](https://api.tartunlp.ai/) from the University of Tartu. This server enables AI assistants and applications to perform high-quality machine translation across 700+ language pairs, with specialized support for European and Finno-Ugric languages.

## Features

- 🌍 **700+ Language Pairs** - Comprehensive translation coverage including European languages and rare Finno-Ugric languages
- 🚀 **Docker-First Deployment** - Pre-built Docker images for easy deployment across platforms
- 🔧 **Simple Integration** - Standard MCP protocol support for seamless integration with AI assistants
- 🎯 **Specialized Language Support** - Expert translation for Estonian, Finnish, Sami languages, and other minority languages
- 📦 **Zero Configuration** - Works out of the box with sensible defaults

## Quick Start

### Using Docker (Recommended)

The easiest way to use this MCP server is via Docker. Pre-built images are automatically published to GitHub Container Registry and support both `linux/amd64` and `linux/arm64` platforms.

Add this configuration to your MCP settings file (e.g., `~/.vscode-server/data/User/mcp.json` or Claude Desktop config):

```json
{
  "mcpServers": {
    "TartuNLP": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ghcr.io/tbitu/tartunlp-mcp:latest"
      ]
    }
  }
}
```

> [!TIP]
> The Docker approach requires no local Python installation or dependency management. The image is kept minimal (~150MB) for fast downloads.

### Using Python (Local Development)

For local development or if you prefer not to use Docker:

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Add to your MCP configuration:**

   **Linux/Mac:**
   ```json
   {
     "mcpServers": {
       "TartuNLP": {
         "command": "python3",
         "args": ["-m", "tartunlp_mcp_server"]
       }
     }
   }
   ```

   **Windows:**
   ```json
   {
     "mcpServers": {
       "TartuNLP": {
         "command": "python",
         "args": ["-m", "tartunlp_mcp_server"]
       }
     }
   }
   ```

> [!NOTE]
> Requires Python 3.8 or higher. Use `python3` on systems where both Python 2 and 3 are installed.

## Available Tools

Once configured, the MCP server exposes the following tools to AI assistants:

### `translate_text`
Translate text between any supported language pair.

**Parameters:**
- `text` (string): The text to translate
- `source_lang` (string): Source language code (e.g., 'eng', 'est', 'fin')
- `target_lang` (string): Target language code (e.g., 'eng', 'est', 'fin')
- `model` (string, optional): Specific translation model/domain to use

### `get_supported_languages`
Retrieve the complete list of supported language pairs and available translation models.

**Returns:** List of all 700+ available translation pairs with source/target language information.

## Development

### Local Testing

```bash
# Install dependencies
pip install -e .

# Run the server locally
python -m tartunlp_mcp_server
```

### Building Docker Images

```bash
# Build locally
docker build -t tartunlp-mcp .

# Test the Docker image
docker run -i --rm tartunlp-mcp
```

### CI/CD

Docker images are automatically built and published to GitHub Container Registry on every push to the `docker-mcp` branch. The workflow:

1. Builds multi-platform images (linux/amd64, linux/arm64)
2. Tags images with branch name, commit SHA, and `latest`
3. Publishes to `ghcr.io/tbitu/tartunlp-mcp`

See [`.github/workflows/docker-build-push.yml`](.github/workflows/docker-build-push.yml) for details.

## Supported Languages

The server supports **700 translation pairs** as provided by TartuNLP's API. Based on the actual API response, the supported language pairs are:

### Core European Languages with Full Coverage
- **English (eng)** ↔ Estonian, German, Lithuanian, Latvian, Finnish, Russian, Ukrainian + all minority languages
- **Estonian (est)** ↔ English, German, Lithuanian, Latvian, Finnish, Russian, Ukrainian + all minority languages  
- **Finnish (fin)** ↔ English, Estonian, German, Lithuanian, Latvian, Russian + all minority languages
- **Russian (rus)** ↔ English, Estonian, German, Lithuanian, Latvian, Finnish, Ukrainian + all minority languages
- **Latvian (lav)** ↔ English, Estonian, German, Lithuanian, Finnish, Russian + all minority languages

### Limited European Language Support
- **German (ger)** ↔ English, Estonian, Lithuanian, Latvian, Finnish, Russian (no minority language pairs)
- **Lithuanian (lit)** ↔ English, Estonian, German, Latvian, Finnish, Russian (no minority language pairs)
- **Ukrainian (ukr)** ↔ English, Estonian, Russian only
- **Norwegian (nor)** ↔ All minority languages only (no major European languages except through minority languages)
- **Hungarian (hun)** ↔ All minority languages only (no major European languages except through minority languages)

### Finno-Ugric & Minority Languages (Full Matrix)
All minority languages can translate to/from each other and to/from: eng, est, fin, rus, lav, nor, hun

- **Karelian (krl)** - Karelian language
- **Ludian (lud)** - Ludic language  
- **Veps (vep)** - Vepsian language
- **Livonian (liv)** - Livonian language (critically endangered)
- **Võro (vro)** - Võro language (South Estonian)
- **Mari (mhr)** - Eastern Mari
- **Hill Mari (mrj)** - Western Mari
- **Udmurt (udm)** - Udmurt language
- **Komi-Permyak (koi)** - Komi-Permyak language
- **Komi-Zyrian (kpv)** - Komi-Zyrian language
- **Moksha (mdf)** - Moksha Mordvin
- **Erzya (myv)** - Erzya Mordvin
- **Olonets (olo)** - Olonets Karelian
- **Mansi (mns)** - Mansi language
- **Khanty (kca)** - Khanty language

### Sami Languages (Full Matrix)
- **Southern Sami (sma)** - Åarjelsaemien gïele
- **Northern Sami (sme)** - Davvisámegiella  
- **Inari Sami (smn)** - Anarâškielâ
- **Skolt Sami (sms)** - Sääʹmǩiõll
- **Lule Sami (smj)** - Julevsámegiella

### Key Translation Patterns

**Major European Language Pairs:**
- eng ↔ est, ger, lit, lav, fin, rus, ukr
- est ↔ eng, ger, lit, lav, fin, rus, ukr  
- fin ↔ eng, est, ger, lit, lav, rus
- rus ↔ eng, est, ger, lit, lav, fin, ukr
- lav ↔ eng, est, ger, lit, fin, rus
- ger ↔ eng, est, lit, lav, fin, rus (limited)
- lit ↔ eng, est, ger, lav, fin, rus (limited)
- ukr ↔ eng, est, rus (very limited)

**Minority Language Hub:**
All 20 minority/indigenous languages form a complete translation matrix with each other and connect to: eng, est, fin, rus, lav, nor, hun

**Note:** The exact language pairs are determined by TartuNLP's API and may be updated. Use the `get_supported_languages` tool to get the current list.

## Tools

- `translate_text`: Translate text between supported languages
- `get_supported_languages`: List all supported language pairs