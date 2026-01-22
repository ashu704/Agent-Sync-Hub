import { Layers } from 'lucide-react';

export function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <div className="logo-icon">
            <Layers size={24} />
          </div>
          <div className="logo-text">
            <h1>Agent-Sync</h1>
            <span>Context Hub</span>
          </div>
        </div>
        <p className="tagline">Universal Neural Layer for AI Development</p>
      </div>
      
      <style>{`
        .header {
          background: var(--bg-secondary);
          border-bottom: 1px solid var(--border-light);
          padding: 16px 24px;
        }
        
        .header-content {
          display: flex;
          align-items: center;
          justify-content: space-between;
          max-width: 1400px;
          margin: 0 auto;
        }
        
        .logo {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        
        .logo-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          background: var(--accent-primary);
          color: white;
          border-radius: var(--radius-sm);
        }
        
        .logo-text h1 {
          font-size: 18px;
          font-weight: 600;
          color: var(--text-primary);
          line-height: 1.2;
        }
        
        .logo-text span {
          font-size: 12px;
          color: var(--text-secondary);
        }
        
        .tagline {
          font-size: 13px;
          color: var(--text-muted);
        }
        
        @media (max-width: 768px) {
          .tagline {
            display: none;
          }
        }
      `}</style>
    </header>
  );
}
