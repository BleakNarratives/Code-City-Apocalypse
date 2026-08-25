import React, { useEffect, useState } from 'react'
import { useAppContext } from '../context/AppContext'
import type { PermissionsState } from '../types'

/**
 * Permissions Gate Component
 * Checks and requests necessary permissions before allowing access
 */

const checkPermission = async (name: 'camera' | 'microphone' | 'notification'): Promise<'granted' | 'denied' | 'prompt' | undefined> => {
  try {
    // Modern Permissions API
    if (navigator.permissions && navigator.permissions.query) {
      const status = await navigator.permissions.query({ name })
      return status.state as 'granted' | 'denied' | 'prompt'
    }
    
    // Fallback: try to access the device
    if (name === 'camera') {
      try {
        await navigator.mediaDevices.getUserMedia({ video: true })
        return 'granted'
      } catch {
        return 'denied'
      }
    }
    
    if (name === 'microphone') {
      try {
        await navigator.mediaDevices.getUserMedia({ audio: true })
        return 'granted'
      } catch {
        return 'denied'
      }
    }
    
    // Notification permission
    if (name === 'notification' && 'Notification' in window) {
      return Notification.permission as 'granted' | 'denied' | 'prompt'
    }
    
  } catch (e) {
    console.warn(`Permission check failed for ${name}:`, e)
  }
  return undefined
}

const requestPermission = async (name: 'camera' | 'microphone' | 'notification'): Promise<boolean> => {
  try {
    if (name === 'camera') {
      await navigator.mediaDevices.getUserMedia({ video: true })
      return true
    }
    
    if (name === 'microphone') {
      await navigator.mediaDevices.getUserMedia({ audio: true })
      return true
    }
    
    if (name === 'notification' && 'Notification' in window) {
      const permission = await Notification.requestPermission()
      return permission === 'granted'
    }
    
  } catch (e) {
    console.warn(`Permission request failed for ${name}:`, e)
    return false
  }
  return false
}

/**
 * Permissions Gate Component
 * Wraps children and only renders them if permissions are granted
 * or simple mode is enabled
 */
export const PermissionsGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { state, dispatch } = useAppContext()
  const [checked, setChecked] = useState(false)

  useEffect(() => {
    (async () => {
      const cam = await checkPermission('camera')
      const mic = await checkPermission('microphone')
      const notification = await checkPermission('notification')
      
      dispatch({
        type: 'SET_PERMISSIONS',
        payload: { camera: cam, microphone: mic, notification }
      })
      setChecked(true)
    })()
  }, [dispatch])

  // Check if permissions are acceptable
  const cameraOk = state.permissions.camera === 'granted' || state.settings.simpleMode
  const micOk = state.permissions.microphone === 'granted' || state.settings.simpleMode
  
  if (!checked) {
    return (
      <div style={{
        padding: 20,
        maxWidth: 720,
        margin: '0 auto',
        textAlign: 'center',
        color: '#64748b'
      }}>
        <div className="spinner" style={{ margin: '0 auto 16px' }} />
        Checking device permissions…
      </div>
    )
  }

  if (cameraOk && micOk) {
    return <>{children}</>
  }

  // Show permissions request UI
  return (
    <div style={{
      padding: 20,
      maxWidth: 720,
      margin: '0 auto',
      background: '#fff',
      borderRadius: 8,
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
    }}>
      <div className="syntax-ai-header">
        <div className="syntax-ai-logo">SA</div>
        <div className="syntax-ai-title">Syntax AI CaptCoder</div>
      </div>
      
      <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>
        Permissions Required
      </h2>
      <p style={{ color: '#64748b', fontSize: 14 }}>
        To use voice, camera, and notification features, we need certain permissions.
        If you prefer not to grant them, switch to Simple Mode.
      </p>

      <div style={{ marginTop: 20, display: 'grid', gap: 16 }}>
        {state.permissions.camera !== 'granted' && (
          <PermissionCard
            name="Camera"
            description="Needed to analyze visual code and capture screenshots."
            onEnable={async () => {
              const granted = await requestPermission('camera')
              if (granted) {
                const cam = await checkPermission('camera')
                dispatch({ 
                  type: 'SET_PERMISSIONS', 
                  payload: { ...state.permissions, camera: cam || 'granted' } 
                })
              } else {
                dispatch({
                  type: 'LOG_ERROR',
                  payload: {
                    id: Date.now().toString(),
                    code: 'CAM_DENY',
                    message: 'Camera permission denied by user',
                    timestamp: new Date().toISOString(),
                    severity: 'info'
                  }
                })
              }
            }}
          />
        )}

        {state.permissions.microphone !== 'granted' && (
          <PermissionCard
            name="Microphone"
            description="Needed for voice commands and hands-free coding."
            onEnable={async () => {
              const granted = await requestPermission('microphone')
              if (granted) {
                const mic = await checkPermission('microphone')
                dispatch({
                  type: 'SET_PERMISSIONS',
                  payload: { ...state.permissions, microphone: mic || 'granted' }
                })
              } else {
                dispatch({
                  type: 'LOG_ERROR',
                  payload: {
                    id: Date.now().toString(),
                    code: 'MIC_DENY',
                    message: 'Microphone permission denied by user',
                    timestamp: new Date().toISOString(),
                    severity: 'info'
                  }
                })
              }
            }}
          />
        )}

        {state.permissions.notification !== 'granted' && (
          <PermissionCard
            name="Notifications"
            description="Needed for alerts and status updates."
            onEnable={async () => {
              const granted = await requestPermission('notification')
              if (granted) {
                const notification = await checkPermission('notification')
                dispatch({
                  type: 'SET_PERMISSIONS',
                  payload: { ...state.permissions, notification: notification || 'granted' }
                })
              }
            }}
          />
        )}
      </div>

      <div style={{ marginTop: 20, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <button 
          className="btn-outline" 
          onClick={() => dispatch({ type: 'TOGGLE_SIMPLE_MODE', payload: true })}
        >
          Switch to Simple Mode (No camera/mic)
        </button>
        <button 
          className="btn" 
          onClick={() => window.location.reload()}
        >
          Retry All
        </button>
      </div>

      <div style={{ 
        marginTop: 16, 
        fontSize: 12, 
        color: '#94a3b8',
        textAlign: 'center'
      }}>
        Note: Permission requirements can be changed in Settings
      </div>
    </div>
  )
}

/**
 * Permission Card Component
 * Displays information about a single permission
 */
interface PermissionCardProps {
  name: string
  description: string
  onEnable: () => Promise<void>
}

const PermissionCard: React.FC<PermissionCardProps> = ({ name, description, onEnable }) => (
  <div style={{
    padding: 16,
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    background: '#fff'
  }}>
    <h3 style={{ fontWeight: 600, marginBottom: 4 }}>{name}</h3>
    <p style={{ fontSize: 13, color: '#64748b', marginBottom: 8 }}>
      {description}
    </p>
    <button 
      className="btn" 
      onClick={onEnable}
      style={{ marginTop: 8 }}
    >
      Enable {name}
    </button>
  </div>
)

export default PermissionsGate
