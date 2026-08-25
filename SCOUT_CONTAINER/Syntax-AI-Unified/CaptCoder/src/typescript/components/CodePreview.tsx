import React from 'react'
import { useAppContext } from '../context/AppContext'
import type { ExtractedCode } from '../types'

/**
 * Code Preview Component
 * Displays extracted code snippets
 */
export const CodePreview: React.FC = () => {
  const { state, dispatch } = useAppContext()

  if (state.extractedCode.length === 0) {
    return null
  }

  return (
    <div className="card" style={{ marginTop: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ fontSize: 16, fontWeight: 600, margin: 0 }}>
          📥 Extracted Code ({state.extractionStats.totalExtracted})
        </h3>
        <button
          className="btn-outline"
          onClick={() => dispatch({ type: 'CLEAR_EXTRACTED_CODE' })}
          style={{ padding: '4px 8px', fontSize: 12 }}
        >
          Clear All
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {state.extractedCode.slice(-5).reverse().map((code: ExtractedCode) => (
          <CodeCard
            key={code.id}
            code={code}
            onRemove={() => dispatch({ type: 'REMOVE_EXTRACTED_CODE', payload: code.id })}
          />
        ))}
        
        {state.extractedCode.length > 5 && (
          <p style={{ fontSize: 12, color: '#94a3b8', textAlign: 'center' }}>
            + {state.extractedCode.length - 5} more snippets
          </p>
        )}
      </div>
    </div>
  )
}

/**
 * Code Card Component
 * Displays a single extracted code snippet
 */
interface CodeCardProps {
  code: ExtractedCode
  onRemove: () => void
}

const CodeCard: React.FC<CodeCardProps> = ({ code, onRemove }) => {
  const languageLabel = code.language || 'unknown'
  const sourceLabel = code.source || 'unknown'
  
  // Truncate long code
  const displayCode = code.code.length > 200 
    ? code.code.substring(0, 200) + '...' 
    : code.code

  return (
    <div style={{
      border: '1px solid var(--border)',
      borderRadius: 8,
      padding: 12,
      background: '#fff',
      position: 'relative'
    }}>
      {/* Header with metadata */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8,
        fontSize: 12
      }}>
        <div style={{ display: 'flex', gap: 8 }}>
          <span style={{
            padding: '2px 6px',
            background: getLanguageColor(languageLabel),
            color: '#fff',
            borderRadius: 4,
            fontSize: 11,
            fontWeight: 500
          }}>
            {languageLabel}
          </span>
          <span style={{ color: '#94a3b8' }}>
            {sourceLabel}
          </span>
          {code.filePath && (
            <span style={{ color: '#64748b' }} title={code.filePath}>
              {code.filePath.split('/').pop()}
            </span>
          )}
        </div>
        
        <button
          onClick={onRemove}
          style={{
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            color: '#94a3b8',
            fontSize: 14,
            padding: '2px 4px'
          }}
          title="Remove"
        >
          ×
        </button>
      </div>

      {/* Code display */}
      <pre style={{
        margin: 0,
        padding: 12,
        background: '#1e293b',
        borderRadius: 6,
        overflowX: 'auto',
        fontSize: 13,
        lineHeight: 1.5
      }}>
        <code style={{ color: '#e2e8f0', fontFamily: 'monospace' }}>
          {displayCode}
        </code>
      </pre>

      {/* Footer with timestamp */}
      <div style={{
        marginTop: 8,
        fontSize: 11,
        color: '#94a3b8',
        display: 'flex',
        justifyContent: 'space-between'
      }}>
        <span>
          Extracted: {new Date(code.timestamp).toLocaleTimeString()}
        </span>
        {code.lineNumber && (
          <span>Line: {code.lineNumber}</span>
        )}
      </div>
    </div>
  )
}

/**
 * Helper function to get language color
 */
function getLanguageColor(language: string): string {
  const colors: Record<string, string> = {
    python: '#3574d4',
    javascript: '#f7df1e',
    typescript: '#3178c6',
    java: '#b07219',
    cpp: '#00599c',
    csharp: '#68217a',
    go: '#00add8',
    rust: '#dea584',
    ruby: '#934959',
    php: '#4f5d95',
    swift: '#fa7343',
    kotlin: '#7f52ff',
    bash: '#89e051',
    html: '#e34c26',
    css: '#563d7c',
    json: '#292929',
    unknown: '#6e7781',
  }
  return colors[language.toLowerCase()] || '#6e7781'
}

export default CodePreview
