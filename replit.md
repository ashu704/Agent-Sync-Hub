# Agent-Sync Context Hub

## Overview
A Streamlit-based AI-powered context hub that generates agnostic .agent configurations for multiple AI coding assistants. Solves "Agent Amnesia" and "IDE Fragmentation" by providing a single source of truth.

## Project Structure
```
├── app.py                 # Main Streamlit application
├── gemini_service.py      # Gemini AI integration for triple-stream analysis
├── generators.py          # File generators for all configurations
├── .streamlit/
│   └── config.toml        # Streamlit server configuration
├── pyproject.toml         # Python dependencies
└── attached_assets/       # PRD and reference documents
```

## Key Features
- **Triple-Stream Analysis**: Anatomy (structure), Metabolism (dependencies), Intent (preferences)
- **Multi-Bridge Generation**: Creates configs for 6+ AI tools (Cursor, GitHub Copilot, Claude Code, Windsurf, JetBrains AI, Google Antigravity)
- **.agent Ecosystem**: Generates rules.json, skills/, mcp_config.json, SESSION_HANDOFF.md
- **AI Readiness Score**: Visual 0-100 score based on project completeness
- **ZIP Export**: Single-click download of all generated files

## Technical Stack
- **Frontend**: Streamlit
- **AI**: Google Gemini (gemini-2.5-flash) via API key
- **Export**: Python zipfile for ZIP generation
- **Config**: YAML and JSON generation

## Running the Application
```bash
streamlit run app.py --server.port 5000
```

## API Key
The application requires a Gemini API key which users enter in the sidebar.

## Recent Changes
- 2026-01-22: Initial implementation with full MVP features
