import { useState } from 'react';
import { FileCode, FileJson, FileText, Folder, ChevronRight, ChevronDown, Copy, Check } from 'lucide-react';
import { GeneratedFile } from '../types';

interface FileExplorerProps {
  files: GeneratedFile[];
}

export function FileExplorer({ files }: FileExplorerProps) {
  const [selectedFile, setSelectedFile] = useState<GeneratedFile | null>(null);
  const [copied, setCopied] = useState(false);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set(['.agent', '.cursor', '.github']));

  if (files.length === 0) {
    return (
      <div className="empty-state">
        <FileCode size={48} strokeWidth={1} />
        <h3>No files generated yet</h3>
        <p>Complete the Context Terminal to generate your configuration files</p>
      </div>
    );
  }

  const fileTree = buildFileTree(files);

  const toggleFolder = (path: string) => {
    setExpandedFolders(prev => {
      const next = new Set(prev);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return next;
    });
  };

  const copyToClipboard = async (content: string) => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'json': return <FileJson size={16} className="icon-json" />;
      case 'markdown': return <FileText size={16} className="icon-md" />;
      default: return <FileCode size={16} className="icon-text" />;
    }
  };

  return (
    <div className="file-explorer">
      <div className="file-tree">
        <h3 className="tree-title">Generated Files</h3>
        <div className="tree-content">
          {renderTree(fileTree, '', expandedFolders, toggleFolder, setSelectedFile, getFileIcon)}
        </div>
      </div>

      <div className="file-preview">
        {selectedFile ? (
          <>
            <div className="preview-header">
              <div className="preview-title">
                {getFileIcon(selectedFile.type)}
                <span>{selectedFile.path}</span>
              </div>
              <button
                className="btn btn-secondary copy-btn"
                onClick={() => copyToClipboard(selectedFile.content)}
              >
                {copied ? <Check size={14} /> : <Copy size={14} />}
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <pre className="preview-content">
              <code>{selectedFile.content}</code>
            </pre>
          </>
        ) : (
          <div className="preview-empty">
            <FileCode size={32} strokeWidth={1} />
            <p>Select a file to preview its contents</p>
          </div>
        )}
      </div>

      <style>{`
        .file-explorer {
          display: grid;
          grid-template-columns: 280px 1fr;
          gap: 20px;
          height: calc(100vh - 200px);
          min-height: 400px;
        }
        
        .file-tree {
          background: var(--bg-secondary);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-md);
          overflow: hidden;
          display: flex;
          flex-direction: column;
        }
        
        .tree-title {
          padding: 14px 16px;
          font-size: 13px;
          font-weight: 600;
          color: var(--text-secondary);
          border-bottom: 1px solid var(--border-light);
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        
        .tree-content {
          flex: 1;
          overflow-y: auto;
          padding: 8px;
        }
        
        .tree-folder, .tree-file {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 12px;
          font-size: 13px;
          border-radius: 6px;
          cursor: pointer;
          transition: background 0.1s ease;
        }
        
        .tree-folder:hover, .tree-file:hover {
          background: var(--bg-tertiary);
        }
        
        .tree-file.selected {
          background: #dbeafe;
          color: #1e40af;
        }
        
        .tree-folder-icon {
          color: #f59e0b;
        }
        
        .tree-children {
          padding-left: 16px;
        }
        
        .icon-json { color: #eab308; }
        .icon-md { color: #6366f1; }
        .icon-text { color: #6b7280; }
        
        .file-preview {
          background: var(--bg-secondary);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-md);
          overflow: hidden;
          display: flex;
          flex-direction: column;
        }
        
        .preview-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 16px;
          border-bottom: 1px solid var(--border-light);
          background: var(--bg-tertiary);
        }
        
        .preview-title {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 13px;
          font-weight: 500;
          color: var(--text-primary);
        }
        
        .copy-btn {
          padding: 6px 12px;
          font-size: 12px;
        }
        
        .preview-content {
          flex: 1;
          overflow: auto;
          padding: 16px;
          margin: 0;
          font-size: 13px;
          line-height: 1.6;
          background: #fafafa;
        }
        
        .preview-content code {
          white-space: pre-wrap;
          word-break: break-word;
        }
        
        .preview-empty {
          flex: 1;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 12px;
          color: var(--text-muted);
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
        
        @media (max-width: 768px) {
          .file-explorer {
            grid-template-columns: 1fr;
            height: auto;
          }
          
          .file-tree {
            max-height: 300px;
          }
          
          .file-preview {
            min-height: 400px;
          }
        }
      `}</style>
    </div>
  );
}

interface TreeNode {
  name: string;
  path: string;
  type: 'folder' | 'file';
  file?: GeneratedFile;
  children: TreeNode[];
}

function buildFileTree(files: GeneratedFile[]): TreeNode[] {
  const root: TreeNode[] = [];

  for (const file of files) {
    const parts = file.path.split('/');
    let current = root;

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      const isFile = i === parts.length - 1;
      const currentPath = parts.slice(0, i + 1).join('/');

      let node = current.find(n => n.name === part);
      if (!node) {
        node = {
          name: part,
          path: currentPath,
          type: isFile ? 'file' : 'folder',
          file: isFile ? file : undefined,
          children: []
        };
        current.push(node);
      }
      current = node.children;
    }
  }

  return root;
}

function renderTree(
  nodes: TreeNode[],
  _parentPath: string,
  expandedFolders: Set<string>,
  toggleFolder: (path: string) => void,
  selectFile: (file: GeneratedFile | null) => void,
  getFileIcon: (type: string) => React.ReactNode
): React.ReactNode {
  return nodes.map(node => {
    if (node.type === 'folder') {
      const isExpanded = expandedFolders.has(node.path);
      return (
        <div key={node.path}>
          <div className="tree-folder" onClick={() => toggleFolder(node.path)}>
            {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            <Folder size={16} className="tree-folder-icon" />
            <span>{node.name}</span>
          </div>
          {isExpanded && node.children.length > 0 && (
            <div className="tree-children">
              {renderTree(node.children, node.path, expandedFolders, toggleFolder, selectFile, getFileIcon)}
            </div>
          )}
        </div>
      );
    }

    return (
      <div
        key={node.path}
        className="tree-file"
        onClick={() => selectFile(node.file || null)}
      >
        {getFileIcon(node.file?.type || 'text')}
        <span>{node.name}</span>
      </div>
    );
  });
}
