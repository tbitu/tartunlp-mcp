# TartuNLP MCP Server

An MCP server that provides access to TartuNLP translation services from the University of Tartu.

## Features

- Text translation between supported language pairs
- Support for multiple TartuNLP translation models
- Batch translation capabilities

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install the package
```bash
pip install -e .
```

## Usage

Add to your MCP configuration file:

### Cross-Platform Configuration

**Option 1: Using python3 (recommended for Linux/Mac)**
```json
{
  "mcpServers": {
    "TartuNLP": {
      "command": "python3",
      "args": ["-m", "tartunlp_mcp_server"],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "translate_text",
        "get_supported_languages"
      ]
    }
  }
}
```

**Option 2: Using python (Windows/cross-platform)**
```json
{
  "mcpServers": {
    "TartuNLP": {
      "command": "python",
      "args": ["-m", "tartunlp_mcp_server"],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "translate_text",
        "get_supported_languages"
      ]
    }
  }
}
```

### Configuration Notes
- Use `python3` on Linux/Mac systems where both Python 2 and 3 are installed
- Use `python` on Windows or systems where Python 3 is the default
- The `autoApprove` array allows automatic execution of translation tools without manual approval

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