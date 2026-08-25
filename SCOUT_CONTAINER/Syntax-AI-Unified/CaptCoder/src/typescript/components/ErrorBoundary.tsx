import React from 'react'
import { useAppContext } from '../context/AppContext'
import type { AppError } from '../types'

/**
 * Error Boundary Component
 * Catches rendering errors and provides graceful fallback UI
 */
class ErrorBoundaryInner extends React.Component<{ onReport?: (err: any, info: any) => void }, { hasError: boolean; error?: any }> {
  constructor(props: any) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: any) {
    return { hasError: true, error }
  }

  componentDidCatch(error: any, info: any) {
    if (this.props.onReport) this.props.onReport(error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: 24,
          textAlign: 'center',
          background: '#fef2f2',
          borderRadius: 8,
          margin: 24
        }}>
          <h2 style={{ fontSize: 20, fontWeight: 700, color: '#dc2626' }}>
            Something went wrong.
          </h2>
          <p style={{ marginTop: 8, color: '#7f1d1d' }}>
            We captured the problem and will help you recover.
          </p>
          <p style={{ marginTop: 8, fontSize: 14, color: '#991b1b' }}>
            Error: {this.state.error?.message || 'Unknown error'}
          </p>
          <div style={{ marginTop: 16, display: 'flex', gap: 8, justifyContent: 'center' }}>
            <button 
              style={{ padding: '8px 12px' }} 
              onClick={() => window.location.reload()}
            >
              Reload Application
            </button>
            <button 
              style={{ padding: '8px 12px', background: 'transparent', border: '1px solid #dc2626', color: '#dc2626' }}
              onClick={() => window.history.back()}
            >
              Go Back
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}

/**
 * Error Boundary with App Context Integration
 */
export const ErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { dispatch } = useAppContext()

  return (
    <ErrorBoundaryInner
      onReport={(err: any, info: any) => {
        const error: AppError = {
          id: Date.now().toString(),
          code: 'RENDER_ERROR',
          message: err?.message || 'Render error occurred',
          details: { error: err, info },
          timestamp: new Date().toISOString(),
          severity: 'error'
        }
        dispatch({ type: 'LOG_ERROR', payload: error })
        console.error('ErrorBoundary caught error:', err, info)
      }}
    >
      {children}
    </ErrorBoundaryInner>
  )
}

export default ErrorBoundary
