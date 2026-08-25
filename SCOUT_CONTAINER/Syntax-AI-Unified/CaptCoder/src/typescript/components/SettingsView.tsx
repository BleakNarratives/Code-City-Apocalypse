import React, { useState } from 'react'
import { useAppContext } from '../context/AppContext'

/**
 * Settings View Component
 * Configuration panel for Syntax AI CaptCoder
 */
export const SettingsView: React.FC = () => {
  const { state, dispatch } = useAppContext()
  const [open, setOpen] = useState<Record<string, boolean>>({
    general: true,
    bsm: false,
    extraction: false,
    optimization: false,
    privacy: false,
    developer: false,
  })

  const toggleSection = (section: string) => {
    setOpen(prev => ({ ...prev, [section]: !prev[section] }))
  }

  return (
    <div>
      <div className="syntax-ai-header" style={{ marginBottom: 16 }}>
        <div className="syntax-ai-logo" style={{ width: 32, height: 32, fontSize: 14 }}>⚙</div>
        <div>
          <h2 style={{ fontSize: 18, fontWeight: 700, margin: 0 }}>Settings</h2>
          <p style={{ fontSize: 12, color: '#64748b', margin: '4px 0 0 0' }}>
            Syntax AI CaptCoder Configuration
          </p>
        </div>
      </div>

      {/* Simple Mode Toggle */}
      <div style={{ marginBottom: 16 }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={state.settings.simpleMode}
            onChange={() => dispatch({ type: 'TOGGLE_SIMPLE_MODE' })}
          />
          <span>Simple Mode (hide advanced features)</span>
        </label>
      </div>

      {/* General Section */}
      <SettingsSection
        title="General"
        isOpen={open.general}
        onToggle={() => toggleSection('general')}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <div>
            <label style={{ display: 'block', fontSize: 13, marginBottom: 4, fontWeight: 500 }}>
              API Key
            </label>
            <input
              className="input"
              value={state.settings.apiKey || ''}
              onChange={(e) => dispatch({ type: 'SET_API_KEY', payload: e.target.value })}
              placeholder="Paste your API key"
              type="password"
            />
            <p style={{ fontSize: 11, color: '#94a3b8', marginTop: 4 }}>
              Your API key is stored locally in your browser
            </p>
          </div>
          
          <div>
            <label style={{ display: 'block', fontSize: 13, marginBottom: 4, fontWeight: 500 }}>
              Theme
            </label>
            <select
              className="input"
              value={state.settings.theme}
              onChange={(e) => dispatch({ 
                type: 'SET_SETTINGS', 
                payload: { theme: e.target.value as 'light' | 'dark' | 'system' } 
              })}
            >
              <option value="system">System</option>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>
          
          <div>
            <label style={{ display: 'block', fontSize: 13, marginBottom: 4, fontWeight: 500 }}>
              Max History
            </label>
            <input
              className="input"
              type="number"
              value={state.settings.maxHistory}
              onChange={(e) => dispatch({ 
                type: 'SET_SETTINGS', 
                payload: { maxHistory: parseInt(e.target.value) || 50 } 
              })}
              min="10"
              max="200"
            />
          </div>
        </div>
      </SettingsSection>

      {/* BSM Section */}
      <SettingsSection
        title="Blue Sky Meeting (BSM)"
        isOpen={open.bsm}
        onToggle={() => toggleSection('bsm')}
      >
        <div style={{ fontSize: 13, color: '#64748b' }}>
          <p style={{ marginBottom: 8 }}>
            Configure Blue Sky Meeting behavior
          </p>
          <p style={{ marginBottom: 16 }}>
            BSM Tag: <code>#bsm</code>
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer' }}>
              <input type="checkbox" checked={state.bsm.isActive} readOnly />
              <span>BSM Active: {state.bsm.isActive ? 'Yes' : 'No'}</span>
            </label>
            
            {state.bsm.startedAt && (
              <p style={{ fontSize: 12, color: '#64748b' }}>
                Started: {new Date(state.bsm.startedAt).toLocaleTimeString()}
              </p>
            )}
            
            <button
              className="btn"
              onClick={() => {
                if (state.bsm.isActive) {
                  dispatch({ type: 'BSM_END' })
                } else {
                  dispatch({ type: 'BSM_START', payload: { title: 'Manual BSM' } })
                }
              }}
              style={{ marginTop: 8 }}
            >
              {state.bsm.isActive ? 'End BSM' : 'Start BSM'}
            </button>
          </div>
        </div>
      </SettingsSection>

      {/* Code Extraction Section */}
      <SettingsSection
        title="Code Extraction"
        isOpen={open.extraction}
        onToggle={() => toggleSection('extraction')}
      >
        <div style={{ fontSize: 13, color: '#64748b' }}>
          <p style={{ marginBottom: 12 }}>
            Configure automatic code extraction
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                checked={state.settings.autoOptimize}
                onChange={() => dispatch({ 
                  type: 'SET_SETTINGS', 
                  payload: { autoOptimize: !state.settings.autoOptimize } 
                })}
              />
              <span>Auto-extract code from monitored directories</span>
            </label>
            
            <label style={{ display: 'block', fontSize: 12, marginBottom: 4, fontWeight: 500 }}>
              Watch Directories
            </label>
            {state.settings.watchDirectories.map((dir, index) => (
              <div key={index} style={{ display: 'flex', gap: 8 }}>
                <input
                  className="input"
                  value={dir}
                  onChange={(e) => {
                    const newDirs = [...state.settings.watchDirectories]
                    newDirs[index] = e.target.value
                    dispatch({ type: 'SET_SETTINGS', payload: { watchDirectories: newDirs } })
                  }}
                  style={{ flex: 1 }}
                />
                <button
                  className="btn-outline"
                  onClick={() => {
                    const newDirs = state.settings.watchDirectories.filter((_, i) => i !== index)
                    dispatch({ type: 'SET_SETTINGS', payload: { watchDirectories: newDirs } })
                  }}
                  style={{ padding: '4px 8px', fontSize: 12 }}
                >
                  ×
                </button>
              </div>
            ))}
            
            <button
              className="btn-outline"
              onClick={() => {
                const newDirs = [...state.settings.watchDirectories, '/storage/emulated/0/scripts']
                dispatch({ type: 'SET_SETTINGS', payload: { watchDirectories: newDirs } })
              }}
              style={{ marginTop: 8 }}
            >
              Add Directory
            </button>
          </div>
        </div>
      </SettingsSection>

      {/* Code Optimization Section */}
      <SettingsSection
        title="Code Optimization"
        isOpen={open.optimization}
        onToggle={() => toggleSection('optimization')}
      >
        <div style={{ fontSize: 13, color: '#64748b' }}>
          <p style={{ marginBottom: 12 }}>
            Configure the "Bitch Work" protocol
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                checked={state.settings.autoOptimize}
                onChange={() => dispatch({ 
                  type: 'SET_SETTINGS', 
                  payload: { autoOptimize: !state.settings.autoOptimize } 
                })}
              />
              <span>Auto-optimize code on save</span>
            </label>
            
            <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
              <p style={{ fontSize: 12, marginBottom: 8 }}>
                <strong>Statistics:</strong>
              </p>
              <p style={{ fontSize: 12, color: '#64748b' }}>
                Files scanned: {state.optimizationStats.filesScanned}
              </p>
              <p style={{ fontSize: 12, color: '#64748b' }}>
                Issues found: {state.optimizationStats.totalIssues}
              </p>
              <p style={{ fontSize: 12, color: '#64748b' }}>
                Fixes applied: {state.optimizationStats.fixesApplied}
              </p>
            </div>
          </div>
        </div>
      </SettingsSection>

      {/* Privacy Section */}
      <SettingsSection
        title="Privacy & Data"
        isOpen={open.privacy}
        onToggle={() => toggleSection('privacy')}
      >
        <div style={{ fontSize: 13, color: '#64748b' }}>
          <p style={{ marginBottom: 8 }}>
            <strong>What we do:</strong> The app processes text, code, and audio to provide intelligent assistance.
          </p>
          <p style={{ marginBottom: 8 }}>
            <strong>API Keys:</strong> Your API key is kept locally in your browser storage. It is not sent to any third-party without your consent.
          </p>
          <p style={{ marginBottom: 8 }}>
            <strong>Telemetry:</strong> Optional, opt-in only. No user content is sent without explicit approval.
          </p>
          
          <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer', marginTop: 12 }}>
            <input type="checkbox" />
            <span>Enable optional telemetry (helps improve app)</span>
          </label>
        </div>
      </SettingsSection>

      {/* Developer Section */}
      {!state.settings.simpleMode && (
        <SettingsSection
          title="Developer"
          isOpen={open.developer}
          onToggle={() => toggleSection('developer')}
        >
          <div style={{ fontSize: 13, color: '#64748b' }}>
            <p style={{ marginBottom: 8 }}>Debug and development tools</p>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ display: 'flex', gap: 8 }}>
                <button
                  className="btn-outline"
                  onClick={() => {
                    if (window.confirm('Clear all local storage?')) {
                      localStorage.clear()
                      window.location.reload()
                    }
                  }}
                  style={{ flex: 1 }}
                >
                  Clear Storage
                </button>
                <button
                  className="btn-outline"
                  onClick={() => dispatch({ type: 'CLEAR_CONVERSATION' })}
                  style={{ flex: 1 }}
                >
                  Clear Chat
                </button>
              </div>
              
              <button
                className="btn-outline"
                onClick={() => dispatch({ type: 'CLEAR_EXTRACTED_CODE' })}
              >
                Clear Extracted Code
              </button>
              
              <button
                className="btn-outline"
                onClick={() => dispatch({ type: 'CLEAR_OPTIMIZATION_RESULTS' })}
              >
                Clear Optimization Results
              </button>
              
              <button
                className="btn"
                onClick={() => dispatch({ type: 'RESET_APP' })}
              >
                Full Reset
              </button>
            </div>
            
            <div style={{ marginTop: 16, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
              <p style={{ fontSize: 12, marginBottom: 4 }}>
                <strong>App Statistics:</strong>
              </p>
              <p style={{ fontSize: 12, color: '#64748b' }}>
                BSM Sessions: {state.stats.bsmSessions}
              </p>
              <p style={{ fontSize: 12, color: '#64748b' }}>
                Code Snippets: {state.stats.codeSnippetsExtracted}
              </p>
              <p style={{ fontSize: 12, color: '#64748b' }}>
                Commands: {state.stats.commandsProcessed}
              </p>
              <p style={{ fontSize: 12, color: '#64748b' }}>
                App started: {new Date(state.stats.appStartTime).toLocaleString()}
              </p>
            </div>
          </div>
        </SettingsSection>
      )}

      {/* Action buttons */}
      <div style={{ marginTop: 16, display: 'flex', gap: 8 }}>
        <button
          className="btn-outline"
          onClick={() => dispatch({ type: 'CLEAR_CONVERSATION' })}
          style={{ flex: 1 }}
        >
          Clear Chat
        </button>
        <button
          className="btn-outline"
          onClick={() => dispatch({ type: 'RESET_APP' })}
          style={{ flex: 1 }}
        >
          Reset App
        </button>
      </div>
    </div>
  )
}

/**
 * Settings Section Component
 * Collapsible section for settings
 */
interface SettingsSectionProps {
  title: string
  isOpen: boolean
  onToggle: () => void
  children: React.ReactNode
}

const SettingsSection: React.FC<SettingsSectionProps> = ({ title, isOpen, onToggle, children }) => (
  <div style={{
    marginTop: 12,
    border: '1px solid var(--border)',
    borderRadius: 8,
    background: '#fff'
  }}>
    <button
      style={{
        width: '100%',
        textAlign: 'left',
        padding: 12,
        background: 'transparent',
        border: 'none',
        cursor: 'pointer',
        fontSize: 14,
        fontWeight: 600,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}
      onClick={onToggle}
    >
      <span>{title}</span>
      <span>{isOpen ? '−' : '+'}</span>
    </button>
    
    {isOpen && (
      <div style={{
        padding: 12,
        borderTop: '1px solid var(--border)',
        paddingTop: 12
      }}>
        {children}
      </div>
    )}
  </div>
)

export default SettingsView
