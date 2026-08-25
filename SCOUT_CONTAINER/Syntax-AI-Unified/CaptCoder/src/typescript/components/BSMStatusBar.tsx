import React from 'react'
import { useAppContext } from '../context/AppContext'

/**
 * BSM Status Bar Component
 * Shows Blue Sky Meeting status and controls
 */
export const BSMStatusBar: React.FC = () => {
  const { state, dispatch } = useAppContext()

  if (!state.bsm.isActive) {
    return null
  }

  // Calculate duration
  const duration = state.bsm.startedAt 
    ? Math.floor((new Date().getTime() - new Date(state.bsm.startedAt).getTime()) / 1000)
    : 0
  
  const minutes = Math.floor(duration / 60)
  const seconds = duration % 60

  return (
    <div style={{
      background: 'linear-gradient(135deg, #2563eb, #7c3aed)',
      color: 'white',
      padding: '12px 16px',
      borderRadius: 8,
      marginBottom: 16,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span className="status-dot" style={{ background: '#10b981' }} />
          <span style={{ fontWeight: 600 }}>
            Blue Sky Meeting Active
          </span>
        </div>
        
        <div style={{ fontSize: 13, opacity: 0.9 }}>
          {state.bsm.title || 'Live Coding Session'}
        </div>
        
        {state.bsm.startedAt && (
          <div style={{ fontSize: 13, opacity: 0.8 }}>
            {minutes}:{seconds.toString().padStart(2, '0')}
          </div>
        )}
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        {state.bsm.livestream?.isLive && (
          <span style={{ 
            fontSize: 12, 
            padding: '4px 8px',
            background: 'rgba(255,255,255,0.2)',
            borderRadius: 4
          }}>
            📡 LIVE
          </span>
        )}
        
        {state.bsm.recording?.isRecording && (
          <span style={{ 
            fontSize: 12, 
            padding: '4px 8px',
            background: 'rgba(255,255,255,0.2)',
            borderRadius: 4
          }}>
            🎥 Recording
          </span>
        )}
        
        <button
          onClick={() => {
            if (window.confirm('End Blue Sky Meeting?')) {
              dispatch({ type: 'BSM_END' })
            }
          }}
          style={{
            background: 'rgba(255,255,255,0.2)',
            color: 'white',
            border: 'none',
            padding: '8px 12px',
            borderRadius: 6,
            cursor: 'pointer',
            fontSize: 13,
            fontWeight: 500,
            transition: 'background 0.2s'
          }}
        >
          End BSM
        </button>
      </div>
    </div>
  )
}

export default BSMStatusBar
