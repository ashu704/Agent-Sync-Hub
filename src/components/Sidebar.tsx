import { Key, Cpu, Gauge, Sparkles } from 'lucide-react';
import { AIProvider, AppState } from '../types';

interface SidebarProps {
  state: AppState;
  providers: AIProvider[];
  updateState: (updates: Partial<AppState>) => void;
}

export function Sidebar({ state, providers, updateState }: SidebarProps) {
  const currentProvider = providers.find(p => p.id === state.provider);

  return (
    <aside className="sidebar">
      <div className="sidebar-section">
        <h3 className="sidebar-title">
          <Sparkles size={16} />
          AI Configuration
        </h3>
        
        <div className="tier-toggle">
          <button
            className={`tier-btn ${state.tier === 'free' ? 'active' : ''}`}
            onClick={() => updateState({ tier: 'free', provider: 'perplexity', model: 'sonar-pro' })}
          >
            Free
          </button>
          <button
            className={`tier-btn ${state.tier === 'custom' ? 'active' : ''}`}
            onClick={() => updateState({ tier: 'custom' })}
          >
            Custom API
          </button>
        </div>

        {state.tier === 'custom' && (
          <>
            <div className="field">
              <label className="label">
                <Cpu size={14} />
                Provider
              </label>
              <select
                className="input select"
                value={state.provider}
                onChange={e => {
                  const provider = providers.find(p => p.id === e.target.value);
                  updateState({
                    provider: e.target.value,
                    model: provider?.models[0] || ''
                  });
                }}
              >
                {providers.filter(p => p.id !== 'perplexity').map(p => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>

            <div className="field">
              <label className="label">Model</label>
              <select
                className="input select"
                value={state.model}
                onChange={e => updateState({ model: e.target.value })}
              >
                {currentProvider?.models.map(m => (
                  <option key={m} value={m}>{m}</option>
                ))}
              </select>
            </div>

            <div className="field">
              <label className="label">
                <Key size={14} />
                API Key
              </label>
              <input
                type="password"
                className="input"
                placeholder="Enter your API key"
                value={state.apiKey}
                onChange={e => updateState({ apiKey: e.target.value })}
              />
            </div>
          </>
        )}

        {state.tier === 'free' && (
          <div className="free-info">
            <p>Using Perplexity Sonar-Pro</p>
            <span>Powered by real-time web intelligence</span>
          </div>
        )}
      </div>

      <div className="sidebar-section">
        <h3 className="sidebar-title">
          <Gauge size={16} />
          AI Readiness
        </h3>
        <div className="score-display">
          <div className="score-circle">
            <svg viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="var(--border-light)"
                strokeWidth="8"
              />
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke={state.readinessScore >= 70 ? 'var(--accent-secondary)' : state.readinessScore >= 40 ? 'var(--accent-warning)' : 'var(--accent-error)'}
                strokeWidth="8"
                strokeDasharray={`${state.readinessScore * 2.83} 283`}
                strokeLinecap="round"
                transform="rotate(-90 50 50)"
                style={{ transition: 'stroke-dasharray 0.3s ease' }}
              />
            </svg>
            <span className="score-value">{state.readinessScore}</span>
          </div>
          <p className="score-label">
            {state.readinessScore >= 70 ? 'Ready to generate' : 
             state.readinessScore >= 40 ? 'Add more context' : 
             'Provide project details'}
          </p>
        </div>
      </div>

      {state.generatedFiles.length > 0 && (
        <div className="sidebar-section">
          <h3 className="sidebar-title">Generated Files</h3>
          <div className="file-count">
            <span className="count">{state.generatedFiles.length}</span>
            <span>files ready</span>
          </div>
        </div>
      )}

      <style>{`
        .sidebar {
          width: 280px;
          background: var(--bg-secondary);
          border-right: 1px solid var(--border-light);
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 24px;
          overflow-y: auto;
        }
        
        .sidebar-section {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }
        
        .sidebar-title {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 13px;
          font-weight: 600;
          color: var(--text-secondary);
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        
        .tier-toggle {
          display: flex;
          gap: 4px;
          padding: 4px;
          background: var(--bg-tertiary);
          border-radius: var(--radius-sm);
        }
        
        .tier-btn {
          flex: 1;
          padding: 8px 12px;
          font-size: 13px;
          font-weight: 500;
          color: var(--text-secondary);
          background: transparent;
          border: none;
          border-radius: 4px;
          transition: all 0.15s ease;
        }
        
        .tier-btn:hover {
          color: var(--text-primary);
        }
        
        .tier-btn.active {
          background: var(--bg-secondary);
          color: var(--accent-primary);
          box-shadow: var(--shadow-sm);
        }
        
        .field {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        
        .field .label {
          display: flex;
          align-items: center;
          gap: 6px;
        }
        
        .free-info {
          padding: 12px;
          background: var(--bg-tertiary);
          border-radius: var(--radius-sm);
        }
        
        .free-info p {
          font-size: 14px;
          font-weight: 500;
          color: var(--text-primary);
        }
        
        .free-info span {
          font-size: 12px;
          color: var(--text-muted);
        }
        
        .score-display {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 12px;
          padding: 16px;
          background: var(--bg-tertiary);
          border-radius: var(--radius-md);
        }
        
        .score-circle {
          position: relative;
          width: 100px;
          height: 100px;
        }
        
        .score-circle svg {
          width: 100%;
          height: 100%;
        }
        
        .score-value {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 28px;
          font-weight: 700;
          color: var(--text-primary);
        }
        
        .score-label {
          font-size: 13px;
          color: var(--text-secondary);
          text-align: center;
        }
        
        .file-count {
          display: flex;
          align-items: baseline;
          gap: 8px;
          padding: 12px;
          background: #dcfce7;
          border-radius: var(--radius-sm);
        }
        
        .file-count .count {
          font-size: 24px;
          font-weight: 700;
          color: #166534;
        }
        
        .file-count span:last-child {
          font-size: 13px;
          color: #166534;
        }
        
        @media (max-width: 1024px) {
          .sidebar {
            width: 240px;
          }
        }
      `}</style>
    </aside>
  );
}
