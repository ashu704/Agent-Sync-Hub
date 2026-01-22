# Agent-Sync Context Hub

## Overview
A Streamlit-based AI-powered context hub that generates agnostic .agent configurations for multiple AI coding assistants. Solves "Agent Amnesia" and "IDE Fragmentation" by providing a single source of truth.

## Project Structure
```
├── app.py                 # Main Streamlit application with dark Command Center theme
├── gemini_service.py      # Gemini AI integration for triple-stream analysis
├── generators.py          # File generators for all configurations
├── .streamlit/
│   └── config.toml        # Streamlit server configuration
├── pyproject.toml         # Python dependencies
└── attached_assets/       # PRD and reference documents
```

## Key Features
- **Dark Command Center Theme**: Deep slate background (#05070a), electric blue accents (#2563eb), glassmorphism effects
- **Triple-Stream Analysis**: Anatomy (structure), Metabolism (dependencies), Intent (preferences)
- **Multi-Bridge Generation**: Creates configs for 6+ AI tools (Cursor, GitHub Copilot, Claude Code, Windsurf, JetBrains AI, Google Antigravity)
- **.agent Ecosystem**: Generates rules.json, skills/, mcp_config.json, SESSION_HANDOFF.md
- **AI Readiness Score**: Real-time visual 0-100 score in sidebar
- **Virtual File Explorer**: Sidebar-based file browser for generated files
- **Agentic Reasoning Logs**: Live processing status during generation
- **IDE Bridge Toggles**: Enable/disable individual bridge outputs
- **Test Your Agent Guide**: Challenge prompts to verify rule compliance
- **ZIP Export**: Single-click download with curl command for terminal setup

## UI Components
- **Context Terminal Tab**: Triple-stream inputs with dropdowns for Tech Stack, Language, Design System, State Management, Architectural Style
- **File Explorer Tab**: Browse generated files with syntax highlighting
- **Test Agent Tab**: Verification prompts for agent compliance testing
- **Export Tab**: Bundle download with setup instructions
- **Sidebar**: API key config, bridge toggles, readiness score, file explorer (after generation)

## Technical Stack
- **Frontend**: Streamlit with custom dark theme CSS
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
- 2026-01-22: Added dark Command Center theme with glassmorphism effects
- 2026-01-22: Added sidebar file explorer and quick actions after generation
- 2026-01-22: Added Tech Stack, Design System, State Management dropdowns
- 2026-01-22: Added Agentic Reasoning Logs with live processing status
- 2026-01-22: Added TEST_YOUR_AGENT.md generation with challenge prompts
- 2026-01-22: Added IDE bridge toggle switches
- 2026-01-22: Initial implementation with full MVP features
