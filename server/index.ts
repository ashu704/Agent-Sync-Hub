import express from 'express';
import cors from 'cors';
import OpenAI from 'openai';

const app = express();
app.use(cors());
app.use(express.json());

interface AIProvider {
  name: string;
  baseURL: string;
  models: string[];
}

const providers: Record<string, AIProvider> = {
  perplexity: {
    name: 'Perplexity',
    baseURL: 'https://api.perplexity.ai',
    models: ['sonar', 'sonar-pro', 'sonar-reasoning-pro']
  },
  openai: {
    name: 'OpenAI',
    baseURL: 'https://api.openai.com/v1',
    models: ['gpt-5', 'gpt-4o', 'gpt-4-turbo']
  },
  anthropic: {
    name: 'Anthropic',
    baseURL: 'https://api.anthropic.com/v1',
    models: ['claude-4.5-sonnet', 'claude-opus']
  },
  gemini: {
    name: 'Google Gemini',
    baseURL: 'https://generativelanguage.googleapis.com/v1beta/openai',
    models: ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-3.0-pro']
  },
  deepseek: {
    name: 'DeepSeek',
    baseURL: 'https://api.deepseek.com',
    models: ['deepseek-chat', 'deepseek-coder', 'deepseek-reasoner']
  }
};

async function callAI(
  provider: string,
  model: string,
  apiKey: string,
  systemPrompt: string,
  userPrompt: string
): Promise<string> {
  const providerConfig = providers[provider];
  if (!providerConfig) {
    throw new Error(`Unknown provider: ${provider}`);
  }

  const client = new OpenAI({
    apiKey,
    baseURL: providerConfig.baseURL
  });

  const response = await client.chat.completions.create({
    model,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ],
    max_tokens: 4096,
    temperature: 0.7
  });

  return response.choices[0]?.message?.content || '';
}

app.get('/api/providers', (_req, res) => {
  const providerList = Object.entries(providers).map(([key, value]) => ({
    id: key,
    name: value.name,
    models: value.models
  }));
  res.json(providerList);
});

app.post('/api/analyze', async (req, res) => {
  try {
    const { provider, model, apiKey, streamType, content, context } = req.body;

    const prompts: Record<string, { system: string; user: string }> = {
      anatomy: {
        system: `You are an expert code architect analyzing project structure. Analyze the provided project anatomy and extract:
1. Key directories and their purposes
2. Main entry points
3. Configuration files
4. Architecture patterns used
5. Module organization

Respond in JSON format with keys: directories, entryPoints, configFiles, patterns, modules`,
        user: `Analyze this project structure:\n\n${content}\n\nAdditional context: ${context || 'None provided'}`
      },
      metabolism: {
        system: `You are an expert dependency analyst. Analyze the provided dependencies and extract:
1. Core frameworks and their versions
2. Development tools
3. Testing frameworks
4. Build tools
5. Potential compatibility issues

Respond in JSON format with keys: frameworks, devTools, testing, buildTools, issues`,
        user: `Analyze these dependencies:\n\n${content}\n\nAdditional context: ${context || 'None provided'}`
      },
      intent: {
        system: `You are an expert at understanding developer intent and coding preferences. Based on the provided preferences, create:
1. Coding style guidelines
2. Architecture recommendations
3. Best practices for the tech stack
4. Team workflow suggestions
5. Quality standards

Respond in JSON format with keys: style, architecture, bestPractices, workflow, qualityStandards`,
        user: `Analyze these preferences:\n\n${content}\n\nAdditional context: ${context || 'None provided'}`
      }
    };

    const prompt = prompts[streamType];
    if (!prompt) {
      return res.status(400).json({ error: 'Invalid stream type' });
    }

    const actualApiKey = provider === 'perplexity' && !apiKey
      ? process.env.PERPLEXITY_API_KEY || ''
      : apiKey;

    if (!actualApiKey) {
      return res.status(400).json({ error: 'API key required' });
    }

    const result = await callAI(provider, model, actualApiKey, prompt.system, prompt.user);
    res.json({ result, streamType });
  } catch (error) {
    console.error('Analysis error:', error);
    res.status(500).json({ error: error instanceof Error ? error.message : 'Analysis failed' });
  }
});

app.post('/api/generate', async (req, res) => {
  try {
    const { provider, model, apiKey, anatomy, metabolism, intent } = req.body;

    const systemPrompt = `You are an expert at generating AI coding assistant configurations. Based on the project analysis, generate a comprehensive .agent configuration that includes:

1. rules.json - Project-specific rules for AI assistants
2. skills.json - Capabilities the AI should have for this project
3. mcp_config.json - Model context protocol configuration
4. SESSION_HANDOFF.md - Session continuity document
5. IDE bridge configs for: Cursor, GitHub Copilot, Claude Code, Windsurf, JetBrains AI, Google Antigravity

Respond with a JSON object containing all generated files with their content.`;

    const userPrompt = `Generate configurations based on:

ANATOMY ANALYSIS:
${JSON.stringify(anatomy, null, 2)}

METABOLISM ANALYSIS:
${JSON.stringify(metabolism, null, 2)}

INTENT ANALYSIS:
${JSON.stringify(intent, null, 2)}`;

    const actualApiKey = provider === 'perplexity' && !apiKey
      ? process.env.PERPLEXITY_API_KEY || ''
      : apiKey;

    if (!actualApiKey) {
      return res.status(400).json({ error: 'API key required' });
    }

    const result = await callAI(provider, model, actualApiKey, systemPrompt, userPrompt);
    res.json({ files: result });
  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({ error: error instanceof Error ? error.message : 'Generation failed' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
