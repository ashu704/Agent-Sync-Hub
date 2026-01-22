# Agent-Sync Context Hub

## Overview
A React + TypeScript AI-powered context hub that generates agnostic .agent configurations for multiple AI coding assistants. Solves "Agent Amnesia" and "IDE Fragmentation" by providing a single source of truth.

## Project Structure
```
├── src/
│   ├── main.tsx              # React entry point
│   ├── App.tsx               # Main application component
│   ├── App.css               # App-level styles
│   ├── index.css             # Global styles (clean-slate minimal theme)
│   ├── types/index.ts        # TypeScript interfaces
│   └── components/
│       ├── Header.tsx        # App header with logo
│       ├── Sidebar.tsx       # AI config, tier toggle, readiness score
│       ├── ContextTerminal.tsx  # Triple-stream inputs
│       ├── FileExplorer.tsx  # Generated file browser
│       └── ExportPanel.tsx   # ZIP download and curl command
├── server/
│   └── index.ts              # Express backend for AI API proxying
├── index.html                # HTML entry point
├── vite.config.js            # Vite configuration
├── tsconfig.json             # TypeScript config (client)
├── tsconfig.server.json      # TypeScript config (server)
└── package.json              # Dependencies
```

## Key Features
- **Clean-Slate Light Theme**: Minimal white/gray backgrounds, subtle shadows, clean typography
- **Two-Tier AI System**:
  - Free: Perplexity Sonar-Pro (server-side API key)
  - Custom: User provides API key for OpenAI, Anthropic, Gemini, DeepSeek
- **AI Models Supported**:
  - OpenAI: GPT-5, GPT-4o, GPT-4-turbo
  - Anthropic: Claude 4.5 Sonnet, Claude Opus
  - Google Gemini: 2.5-flash, 2.5-pro, 3.0-pro
  - DeepSeek: DeepSeek Chat, DeepSeek Coder, DeepSeek Reasoner
  - Perplexity: Sonar, Sonar-Pro, Sonar-Reasoning-Pro
- **Triple-Stream Analysis**: Anatomy (structure), Metabolism (dependencies), Intent (preferences)
- **Multi-Bridge Generation**: Configs for Cursor, GitHub Copilot, Claude Code, Windsurf, JetBrains AI
- **Real-time AI Readiness Score**: Visual 0-100 score in sidebar
- **File Explorer**: Browse generated files with syntax highlighting
- **ZIP Export**: Download with curl command for terminal setup

## Technical Stack
- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: Express + TypeScript (tsx)
- **AI Integration**: OpenAI SDK (compatible with all providers)
- **Export**: JSZip + FileSaver
- **Icons**: Lucide React

## Running the Application
The app runs with two processes:
1. Vite dev server on port 5000 (frontend)
2. Express API server on port 3001 (backend)

Command: `npm run dev` (runs both concurrently)

## Environment Variables
- `PERPLEXITY_API_KEY`: Required for free tier (set as secret)
- Custom API keys are provided by users in the UI

## API Endpoints
- `GET /api/providers`: List available AI providers and models
- `POST /api/analyze`: Analyze project stream (anatomy/metabolism/intent)
- `POST /api/generate`: Generate full .agent configuration

## Recent Changes
- 2026-01-22: Rebuilt in React + TypeScript with clean-slate minimal light theme
- 2026-01-22: Added two-tier AI system (free Perplexity, custom API keys)
- 2026-01-22: Added support for OpenAI, Anthropic, Gemini, DeepSeek models
- 2026-01-22: Express backend for secure API proxying
