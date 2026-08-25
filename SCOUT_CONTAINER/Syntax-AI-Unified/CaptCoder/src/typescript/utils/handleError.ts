/**
 * Error Handling Utilities for Syntax AI CaptCoder
 * Integrated from phase_1_v_2/src/utils/handleError.ts
 */

import { useAppContext } from '../context/AppContext'
import type { AppError } from '../types'

/**
 * Format error for consistent representation
 */
export function formatError(e: any): { message: string; code: string; details?: any } {
  if (!e) return { message: 'Unknown error', code: 'UNKNOWN' }
  if (e instanceof Error) return { 
    message: e.message, 
    code: (e as any).code || 'ERR',
    details: e.stack
  }
  if (typeof e === 'string') return { message: e, code: 'ERR_STRING' }
  if (typeof e === 'object') return { 
    message: JSON.stringify(e), 
    code: 'ERR_JSON'
  }
  return { message: String(e), code: 'ERR_UNKNOWN' }
}

/**
 * Hook to handle errors with app context integration
 */
export function useHandleError() {
  const { dispatch } = useAppContext()
  
  return (err: any, opts?: { 
    userMessage?: string; 
    code?: string; 
    severity?: 'info' | 'warning' | 'error' | 'critical' 
  }) => {
    const formatted = formatError(err)
    
    const error: AppError = {
      id: Date.now().toString(),
      code: opts?.code ?? formatted.code,
      message: opts?.userMessage ?? formatted.message,
      details: formatted.details,
      timestamp: new Date().toISOString(),
      severity: opts?.severity ?? 'error'
    }
    
    dispatch({ type: 'LOG_ERROR', payload: error })
    
    // Return the error ID for reference
    return error.id
  }
}

/**
 * Create an error object
 */
export function createError(opts: { 
  message: string; 
  code?: string; 
  details?: any;
  severity?: 'info' | 'warning' | 'error' | 'critical'
}): AppError {
  return {
    id: Date.now().toString(),
    code: opts.code ?? 'UNKNOWN',
    message: opts.message,
    details: opts.details,
    timestamp: new Date().toISOString(),
    severity: opts.severity ?? 'error'
  }
}

/**
 * Log an error to the console with consistent format
 */
export function logError(error: AppError, context?: string): void {
  console.groupCollapsed(`[${error.severity.toUpperCase()}] ${error.code}: ${error.message}`)
  if (context) console.log('Context:', context)
  console.log('Timestamp:', error.timestamp)
  if (error.details) console.log('Details:', error.details)
  console.groupEnd()
}

/**
 * Check if an error is of a specific type
 */
export function isError(error: any, code?: string): error is AppError {
  return error && 
    typeof error === 'object' && 
    'id' in error && 
    'code' in error && 
    'message' in error &&
    (code ? error.code === code : true)
}

export default {
  formatError,
  useHandleError,
  createError,
  logError,
  isError,
}
