import { useState, useEffect, useCallback } from 'react';
import { Settings, FileCode, Download, Loader2, AlertCircle } from 'lucide-react';
import { AIProvider, AppState, GeneratedFile } from './types';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { ContextTerminal } from './components/ContextTerminal';
import { FileExplorer } from './components/FileExplorer';
import { ExportPanel } from './components/ExportPanel';
import './App.css';

const initialState: AppState = {
  tier: 'free',
  provider: 'perplexity',
  model: 'sonar-pro',
  apiKey: '',
  anatomyInput: '',
  metabolismInput: '',
  intentInput: '',
  intentSelections: {
    techStack: 'React + Node.js',
    primaryLanguage: 'TypeScript',
    designSystem: 'Tailwind CSS',
    stateManagement: 'React Context',
    architecturalStyle: 'Monolith'
  },
  analysisResult: null,
  generatedFiles: [],
  readinessScore: 0,
  isAnalyzing: false,
  isGenerating: false,
  currentStep: '',
  error: null
};

type TabId = 'terminal' | 'explorer' | 'export';

export default function App() {
  const [state, setState] = useState<AppState>(initialState);
  const [providers, setProviders] = useState<AIProvider[]>([]);
  const [activeTab, setActiveTab] = useState<TabId>('terminal');

  useEffect(() => {
    fetch('/api/providers')
      .then(res => res.json())
      .then(setProviders)
      .catch(console.error);
  }, []);

  const updateState = useCallback((updates: Partial<AppState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }, []);

  const calculateReadinessScore = useCallback(() => {
    let score = 0;
    if (state.anatomyInput.length > 50) score += 25;
    else if (state.anatomyInput.length > 20) score += 15;
    if (state.metabolismInput.length > 30) score += 25;
    else if (state.metabolismInput.length > 10) score += 15;
    if (state.intentInput.length > 30) score += 20;
    else if (state.intentInput.length > 10) score += 10;
    if (state.intentSelections.techStack !== 'Other') score += 10;
    if (state.intentSelections.primaryLanguage !== 'Other') score += 10;
    if (state.intentSelections.designSystem !== 'Custom/None') score += 5;
    if (state.intentSelections.stateManagement !== 'None/Local State') score += 5;
    return Math.min(100, score);
  }, [state.anatomyInput, state.metabolismInput, state.intentInput, state.intentSelections]);

  useEffect(() => {
    updateState({ readinessScore: calculateReadinessScore() });
  }, [calculateReadinessScore, updateState]);

  const handleAnalyze = async () => {
    updateState({ isAnalyzing: true, error: null, currentStep: 'Starting analysis...' });

    try {
      const apiKey = state.tier === 'custom' ? state.apiKey : '';
      const streams = ['anatomy', 'metabolism', 'intent'];
      const results: Record<string, unknown> = {};

      for (const streamType of streams) {
        updateState({ currentStep: `Analyzing ${streamType}...` });
        
        let content = '';
        if (streamType === 'anatomy') content = state.anatomyInput;
        else if (streamType === 'metabolism') content = state.metabolismInput;
        else content = `${state.intentInput}\n\nPreferences:\n- Tech Stack: ${state.intentSelections.techStack}\n- Language: ${state.intentSelections.primaryLanguage}\n- Design System: ${state.intentSelections.designSystem}\n- State Management: ${state.intentSelections.stateManagement}\n- Architecture: ${state.intentSelections.architecturalStyle}`;

        const response = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            provider: state.provider,
            model: state.model,
            apiKey,
            streamType,
            content,
            context: ''
          })
        });

        if (!response.ok) {
          const err = await response.json();
          throw new Error(err.error || 'Analysis failed');
        }

        const data = await response.json();
        try {
          results[streamType] = JSON.parse(data.result);
        } catch {
          results[streamType] = { raw: data.result };
        }
      }

      updateState({
        analysisResult: results,
        currentStep: 'Generating configurations...',
        isGenerating: true
      });

      const generateResponse = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider: state.provider,
          model: state.model,
          apiKey,
          anatomy: results.anatomy,
          metabolism: results.metabolism,
          intent: results.intent
        })
      });

      if (!generateResponse.ok) {
        const err = await generateResponse.json();
        throw new Error(err.error || 'Generation failed');
      }

      const generateData = await generateResponse.json();
      const files = parseGeneratedFiles(generateData.files);

      updateState({
        generatedFiles: files,
        isAnalyzing: false,
        isGenerating: false,
        currentStep: 'Complete!',
        readinessScore: 100
      });

      setTimeout(() => setActiveTab('explorer'), 500);
    } catch (error) {
      updateState({
        error: error instanceof Error ? error.message : 'An error occurred',
        isAnalyzing: false,
        isGenerating: false,
        currentStep: ''
      });
    }
  };

  const parseGeneratedFiles = (filesData: string): GeneratedFile[] => {
    try {
      const parsed = JSON.parse(filesData);
      const files: GeneratedFile[] = [];
      
      const processObject = (obj: Record<string, unknown>, prefix = '.agent/') => {
        for (const [key, value] of Object.entries(obj)) {
          if (typeof value === 'string') {
            const path = prefix + key;
            const type = key.endsWith('.json') ? 'json' : 
                        key.endsWith('.yaml') || key.endsWith('.yml') ? 'yaml' :
                        key.endsWith('.md') ? 'markdown' : 'text';
            files.push({ path, content: value, type });
          } else if (typeof value === 'object' && value !== null) {
            processObject(value as Record<string, unknown>, prefix + key + '/');
          }
        }
      };
      
      processObject(parsed);
      return files.length > 0 ? files : generateDefaultFiles();
    } catch {
      return generateDefaultFiles();
    }
  };

  const generateDefaultFiles = (): GeneratedFile[] => {
    const { intentSelections, anatomyInput, metabolismInput, intentInput } = state;
    
    return [
      {
        path: '.agent/rules.json',
        content: JSON.stringify({
          version: '1.0',
          project: {
            techStack: intentSelections.techStack,
            language: intentSelections.primaryLanguage,
            designSystem: intentSelections.designSystem,
            stateManagement: intentSelections.stateManagement,
            architecture: intentSelections.architecturalStyle
          },
          rules: [
            { id: 'style-001', rule: `Use ${intentSelections.primaryLanguage} for all new code` },
            { id: 'style-002', rule: `Follow ${intentSelections.designSystem} conventions` },
            { id: 'arch-001', rule: `Maintain ${intentSelections.architecturalStyle} architecture` }
          ]
        }, null, 2),
        type: 'json'
      },
      {
        path: '.agent/skills/code-review.json',
        content: JSON.stringify({
          name: 'Code Review',
          description: `Review code for ${intentSelections.techStack} best practices`,
          triggers: ['review', 'check', 'validate'],
          actions: ['lint', 'format', 'suggest']
        }, null, 2),
        type: 'json'
      },
      {
        path: '.agent/mcp_config.json',
        content: JSON.stringify({
          version: '1.0',
          context: {
            anatomy: anatomyInput.substring(0, 500),
            metabolism: metabolismInput.substring(0, 500),
            intent: intentInput.substring(0, 500)
          },
          preferences: intentSelections
        }, null, 2),
        type: 'json'
      },
      {
        path: '.agent/SESSION_HANDOFF.md',
        content: `# Session Handoff\n\n## Project Context\n- **Tech Stack**: ${intentSelections.techStack}\n- **Language**: ${intentSelections.primaryLanguage}\n- **Design System**: ${intentSelections.designSystem}\n- **State Management**: ${intentSelections.stateManagement}\n- **Architecture**: ${intentSelections.architecturalStyle}\n\n## Current State\nConfiguration generated and ready for use.\n\n## Next Steps\n1. Review generated rules\n2. Customize for your specific needs\n3. Test with your AI assistant`,
        type: 'markdown'
      },
      {
        path: '.agent/TEST_YOUR_AGENT.md',
        content: `# Test Your Agent\n\n## Challenge Prompts\n\n### 1. Style Compliance\nAsk: "Create a new component"\nExpected: Should use ${intentSelections.primaryLanguage} and ${intentSelections.designSystem}\n\n### 2. Architecture Awareness\nAsk: "Where should I add a new feature?"\nExpected: Should follow ${intentSelections.architecturalStyle} patterns\n\n### 3. State Management\nAsk: "How should I manage this data?"\nExpected: Should suggest ${intentSelections.stateManagement}\n\n### 4. Dependency Awareness\nAsk: "Can I add a new library?"\nExpected: Should check compatibility with ${intentSelections.techStack}`,
        type: 'markdown'
      },
      {
        path: '.cursor/rules',
        content: `# Cursor Rules\n\nProject: ${intentSelections.techStack}\nLanguage: ${intentSelections.primaryLanguage}\nDesign: ${intentSelections.designSystem}\n\nAlways follow project conventions.`,
        type: 'text'
      },
      {
        path: '.github/copilot-instructions.md',
        content: `# GitHub Copilot Instructions\n\nThis project uses:\n- ${intentSelections.techStack}\n- ${intentSelections.primaryLanguage}\n- ${intentSelections.designSystem}\n- ${intentSelections.stateManagement}\n\nFollow ${intentSelections.architecturalStyle} patterns.`,
        type: 'markdown'
      },
      {
        path: 'CLAUDE.md',
        content: `# Claude Code Context\n\n## Tech Stack\n${intentSelections.techStack}\n\n## Language\n${intentSelections.primaryLanguage}\n\n## Architecture\n${intentSelections.architecturalStyle}\n\n## Preferences\n${intentInput}`,
        type: 'markdown'
      }
    ];
  };

  const tabs = [
    { id: 'terminal' as const, label: 'Context Terminal', icon: Settings },
    { id: 'explorer' as const, label: 'File Explorer', icon: FileCode },
    { id: 'export' as const, label: 'Export', icon: Download }
  ];

  return (
    <div className="app">
      <Header />
      
      <div className="app-layout">
        <Sidebar
          state={state}
          providers={providers}
          updateState={updateState}
        />
        
        <main className="main-content">
          <nav className="tabs">
            {tabs.map(tab => (
              <button
                key={tab.id}
                className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <tab.icon size={16} />
                {tab.label}
              </button>
            ))}
          </nav>

          <div className="tab-content">
            {activeTab === 'terminal' && (
              <ContextTerminal
                state={state}
                updateState={updateState}
                onAnalyze={handleAnalyze}
              />
            )}
            
            {activeTab === 'explorer' && (
              <FileExplorer files={state.generatedFiles} />
            )}
            
            {activeTab === 'export' && (
              <ExportPanel files={state.generatedFiles} />
            )}
          </div>

          {(state.isAnalyzing || state.isGenerating) && (
            <div className="status-bar">
              <Loader2 className="spin" size={16} />
              <span>{state.currentStep}</span>
            </div>
          )}

          {state.error && (
            <div className="error-bar">
              <AlertCircle size={16} />
              <span>{state.error}</span>
              <button onClick={() => updateState({ error: null })}>Dismiss</button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
