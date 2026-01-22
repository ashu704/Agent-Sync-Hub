import { Zap, FolderTree, Package, Target } from 'lucide-react';
import { AppState, IntentSelections, TECH_STACKS, LANGUAGES, DESIGN_SYSTEMS, STATE_MANAGEMENT, ARCHITECTURAL_STYLES } from '../types';

interface ContextTerminalProps {
  state: AppState;
  updateState: (updates: Partial<AppState>) => void;
  onAnalyze: () => void;
}

export function ContextTerminal({ state, updateState, onAnalyze }: ContextTerminalProps) {
  const updateIntent = (key: keyof IntentSelections, value: string) => {
    updateState({
      intentSelections: { ...state.intentSelections, [key]: value }
    });
  };

  const isReady = state.anatomyInput.length > 10 && 
                  state.metabolismInput.length > 10 && 
                  (state.tier === 'free' || state.apiKey.length > 0);

  return (
    <div className="context-terminal">
      <div className="streams-grid">
        <div className="stream-card">
          <div className="stream-header">
            <div className="stream-icon anatomy">
              <FolderTree size={18} />
            </div>
            <div>
              <h3>Anatomy Stream</h3>
              <p>Project structure & file organization</p>
            </div>
          </div>
          <textarea
            className="input textarea"
            placeholder="Paste your project tree structure, file organization, or describe your folder hierarchy..."
            value={state.anatomyInput}
            onChange={e => updateState({ anatomyInput: e.target.value })}
          />
          <div className="stream-hint">
            Example: src/, components/, pages/, api/, lib/
          </div>
        </div>

        <div className="stream-card">
          <div className="stream-header">
            <div className="stream-icon metabolism">
              <Package size={18} />
            </div>
            <div>
              <h3>Metabolism Stream</h3>
              <p>Dependencies & package ecosystem</p>
            </div>
          </div>
          <textarea
            className="input textarea"
            placeholder="Paste your package.json dependencies, requirements.txt, or list your key libraries..."
            value={state.metabolismInput}
            onChange={e => updateState({ metabolismInput: e.target.value })}
          />
          <div className="stream-hint">
            Example: react, express, prisma, tailwindcss
          </div>
        </div>

        <div className="stream-card intent-card">
          <div className="stream-header">
            <div className="stream-icon intent">
              <Target size={18} />
            </div>
            <div>
              <h3>Intent Stream</h3>
              <p>Preferences & coding standards</p>
            </div>
          </div>
          
          <div className="intent-selectors">
            <div className="selector-row">
              <div className="selector-field">
                <label className="label">Tech Stack</label>
                <select
                  className="input select"
                  value={state.intentSelections.techStack}
                  onChange={e => updateIntent('techStack', e.target.value)}
                >
                  {TECH_STACKS.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
              <div className="selector-field">
                <label className="label">Primary Language</label>
                <select
                  className="input select"
                  value={state.intentSelections.primaryLanguage}
                  onChange={e => updateIntent('primaryLanguage', e.target.value)}
                >
                  {LANGUAGES.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="selector-row">
              <div className="selector-field">
                <label className="label">Design System</label>
                <select
                  className="input select"
                  value={state.intentSelections.designSystem}
                  onChange={e => updateIntent('designSystem', e.target.value)}
                >
                  {DESIGN_SYSTEMS.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
              <div className="selector-field">
                <label className="label">State Management</label>
                <select
                  className="input select"
                  value={state.intentSelections.stateManagement}
                  onChange={e => updateIntent('stateManagement', e.target.value)}
                >
                  {STATE_MANAGEMENT.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="selector-row single">
              <div className="selector-field">
                <label className="label">Architectural Style</label>
                <select
                  className="input select"
                  value={state.intentSelections.architecturalStyle}
                  onChange={e => updateIntent('architecturalStyle', e.target.value)}
                >
                  {ARCHITECTURAL_STYLES.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <textarea
            className="input textarea"
            placeholder="Additional preferences: coding conventions, team guidelines, specific patterns to follow..."
            value={state.intentInput}
            onChange={e => updateState({ intentInput: e.target.value })}
          />
        </div>
      </div>

      <div className="action-area">
        <button
          className="btn btn-primary analyze-btn"
          onClick={onAnalyze}
          disabled={!isReady || state.isAnalyzing || state.isGenerating}
        >
          <Zap size={18} />
          {state.isAnalyzing ? 'Analyzing...' : state.isGenerating ? 'Generating...' : 'Generate Configuration'}
        </button>
        {!isReady && (
          <p className="action-hint">
            {state.tier === 'custom' && !state.apiKey ? 'Enter your API key to continue' : 'Add project context to enable generation'}
          </p>
        )}
      </div>

      <style>{`
        .context-terminal {
          display: flex;
          flex-direction: column;
          gap: 24px;
        }
        
        .streams-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 20px;
        }
        
        .stream-card {
          background: var(--bg-secondary);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-md);
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        
        .intent-card {
          grid-column: span 2;
        }
        
        .stream-header {
          display: flex;
          align-items: flex-start;
          gap: 12px;
        }
        
        .stream-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          border-radius: var(--radius-sm);
          flex-shrink: 0;
        }
        
        .stream-icon.anatomy {
          background: #dbeafe;
          color: #2563eb;
        }
        
        .stream-icon.metabolism {
          background: #dcfce7;
          color: #16a34a;
        }
        
        .stream-icon.intent {
          background: #fef3c7;
          color: #d97706;
        }
        
        .stream-header h3 {
          font-size: 15px;
          font-weight: 600;
          color: var(--text-primary);
        }
        
        .stream-header p {
          font-size: 13px;
          color: var(--text-muted);
        }
        
        .stream-hint {
          font-size: 12px;
          color: var(--text-muted);
          padding-top: 4px;
        }
        
        .intent-selectors {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }
        
        .selector-row {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 16px;
        }
        
        .selector-row.single {
          grid-template-columns: 1fr;
          max-width: 50%;
        }
        
        .selector-field {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        
        .action-area {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 12px;
          padding: 24px;
          background: var(--bg-tertiary);
          border-radius: var(--radius-md);
        }
        
        .analyze-btn {
          padding: 14px 32px;
          font-size: 15px;
        }
        
        .action-hint {
          font-size: 13px;
          color: var(--text-muted);
        }
        
        @media (max-width: 768px) {
          .streams-grid {
            grid-template-columns: 1fr;
          }
          
          .intent-card {
            grid-column: span 1;
          }
          
          .selector-row {
            grid-template-columns: 1fr;
          }
          
          .selector-row.single {
            max-width: 100%;
          }
        }
      `}</style>
    </div>
  );
}
