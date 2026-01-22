import { useState } from 'react';
import { Download, Terminal, Package, Check, Copy } from 'lucide-react';
import { GeneratedFile } from '../types';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

interface ExportPanelProps {
  files: GeneratedFile[];
}

export function ExportPanel({ files }: ExportPanelProps) {
  const [copied, setCopied] = useState(false);

  if (files.length === 0) {
    return (
      <div className="empty-state">
        <Package size={48} strokeWidth={1} />
        <h3>Nothing to export yet</h3>
        <p>Generate your configuration first using the Context Terminal</p>
      </div>
    );
  }

  const handleDownload = async () => {
    const zip = new JSZip();
    
    for (const file of files) {
      zip.file(file.path, file.content);
    }
    
    const blob = await zip.generateAsync({ type: 'blob' });
    const timestamp = new Date().toISOString().slice(0, 10);
    saveAs(blob, `agent-sync-${timestamp}.zip`);
  };

  const curlCommand = `curl -L https://your-replit-url/api/download -o agent-sync.zip && unzip agent-sync.zip`;

  const copyCommand = async () => {
    await navigator.clipboard.writeText(curlCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="export-panel">
      <div className="export-header">
        <h2>Export Configuration</h2>
        <p>Download your complete .agent ecosystem bundle</p>
      </div>

      <div className="export-stats">
        <div className="stat">
          <span className="stat-value">{files.length}</span>
          <span className="stat-label">Files Generated</span>
        </div>
        <div className="stat">
          <span className="stat-value">{files.filter(f => f.path.startsWith('.agent')).length}</span>
          <span className="stat-label">Core Configs</span>
        </div>
        <div className="stat">
          <span className="stat-value">{files.filter(f => !f.path.startsWith('.agent')).length}</span>
          <span className="stat-label">IDE Bridges</span>
        </div>
      </div>

      <div className="export-actions">
        <button className="btn btn-success download-btn" onClick={handleDownload}>
          <Download size={20} />
          Download ZIP Bundle
        </button>
      </div>

      <div className="curl-section">
        <h3>
          <Terminal size={18} />
          Terminal Setup
        </h3>
        <p>Or use this command to download and extract directly:</p>
        <div className="curl-command">
          <code>{curlCommand}</code>
          <button className="copy-btn" onClick={copyCommand}>
            {copied ? <Check size={16} /> : <Copy size={16} />}
          </button>
        </div>
      </div>

      <div className="files-summary">
        <h3>Files Included</h3>
        <ul>
          {files.map(file => (
            <li key={file.path}>
              <span className="file-path">{file.path}</span>
              <span className="badge">{file.type}</span>
            </li>
          ))}
        </ul>
      </div>

      <style>{`
        .export-panel {
          max-width: 800px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 32px;
        }
        
        .export-header {
          text-align: center;
        }
        
        .export-header h2 {
          font-size: 24px;
          font-weight: 600;
          color: var(--text-primary);
          margin-bottom: 8px;
        }
        
        .export-header p {
          font-size: 15px;
          color: var(--text-secondary);
        }
        
        .export-stats {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 16px;
        }
        
        .stat {
          background: var(--bg-secondary);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-md);
          padding: 20px;
          text-align: center;
        }
        
        .stat-value {
          display: block;
          font-size: 32px;
          font-weight: 700;
          color: var(--accent-primary);
        }
        
        .stat-label {
          font-size: 13px;
          color: var(--text-secondary);
        }
        
        .export-actions {
          display: flex;
          justify-content: center;
        }
        
        .download-btn {
          padding: 16px 40px;
          font-size: 16px;
        }
        
        .curl-section {
          background: var(--bg-secondary);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-md);
          padding: 20px;
        }
        
        .curl-section h3 {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 15px;
          font-weight: 600;
          color: var(--text-primary);
          margin-bottom: 8px;
        }
        
        .curl-section > p {
          font-size: 13px;
          color: var(--text-secondary);
          margin-bottom: 12px;
        }
        
        .curl-command {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 16px;
          background: #1a1a1a;
          border-radius: var(--radius-sm);
        }
        
        .curl-command code {
          flex: 1;
          font-size: 13px;
          color: #10b981;
          word-break: break-all;
        }
        
        .curl-command .copy-btn {
          padding: 6px;
          background: transparent;
          border: none;
          color: #6b7280;
          cursor: pointer;
          border-radius: 4px;
        }
        
        .curl-command .copy-btn:hover {
          color: white;
          background: rgba(255, 255, 255, 0.1);
        }
        
        .files-summary {
          background: var(--bg-secondary);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-md);
          padding: 20px;
        }
        
        .files-summary h3 {
          font-size: 15px;
          font-weight: 600;
          color: var(--text-primary);
          margin-bottom: 16px;
        }
        
        .files-summary ul {
          list-style: none;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        
        .files-summary li {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 10px 14px;
          background: var(--bg-tertiary);
          border-radius: var(--radius-sm);
        }
        
        .file-path {
          font-size: 13px;
          font-family: 'JetBrains Mono', monospace;
          color: var(--text-primary);
        }
        
        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 16px;
          padding: 60px;
          color: var(--text-muted);
          text-align: center;
        }
        
        .empty-state h3 {
          font-size: 18px;
          color: var(--text-secondary);
        }
        
        .empty-state p {
          font-size: 14px;
        }
        
        @media (max-width: 640px) {
          .export-stats {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}
