import React, { createContext, useReducer, useContext, useEffect } from 'react'
import type { AppState, AppAction, Message, ExtractedCode, OptimizationResult, PermissionsState, SettingsState, AppStatistics, BSMState } from '../types'

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialBSMState: BSMState = {
  isActive: false,
}

const initialPermissionsState: PermissionsState = {
  camera: undefined,
  microphone: undefined,
  notification: undefined,
}

const initialSettingsState: SettingsState = {
  simpleMode: false,
  apiKey: null,
  theme: 'system',
  enableTTS: true,
  enableSound: true,
  maxHistory: 50,
  autoOptimize: false,
  watchDirectories: ['/storage/emulated/0/Download', '/storage/emulated/0/Documents'],
}

const initialStatistics: AppStatistics = {
  bsmSessions: 0,
  totalBSMDuration: 0,
  codeSnippetsExtracted: 0,
  filesMonitored: 0,
  issuesFound: 0,
  issuesFixed: 0,
  commandsProcessed: 0,
  nexusRequests: 0,
  appStartTime: new Date().toISOString(),
  lastActivity: new Date().toISOString(),
}

const initialState: AppState = {
  conversation: [],
  bsm: initialBSMState,
  extractedCode: [],
  extractionStats: {
    totalExtracted: 0,
    byLanguage: {},
    bySource: {},
  },
  optimizationResults: [],
  optimizationStats: {
    filesScanned: 0,
    filesWithIssues: 0,
    totalIssues: 0,
    issuesByType: {},
    fixesApplied: 0,
  },
  isLoading: false,
  permissions: initialPermissionsState,
  settings: initialSettingsState,
  stats: initialStatistics,
}

// ============================================================================
// ACTION TYPES
// ============================================================================

type Action =
  | AppAction

// ============================================================================
// REDUCER
// ============================================================================

function reducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    // Conversation actions
    case 'ADD_MESSAGE': {
      const nextConv = [...state.conversation, action.payload]
      const capped = nextConv.slice(-state.settings.maxHistory)
      return {
        ...state,
        conversation: capped,
        stats: { ...state.stats, lastActivity: new Date().toISOString() }
      }
    }
    case 'UPDATE_MESSAGE': {
      const updated = state.conversation.map(m =>
        m.id === action.payload.id ? { ...m, ...action.payload.updates } : m
      )
      return { ...state, conversation: updated }
    }
    case 'REMOVE_MESSAGE': {
      return {
        ...state,
        conversation: state.conversation.filter(m => m.id !== action.payload)
      }
    }
    case 'CLEAR_CONVERSATION': {
      return { ...state, conversation: [] }
    }

    // BSM actions
    case 'BSM_START': {
      return {
        ...state,
        bsm: { ...state.bsm, isActive: true, startedAt: new Date().toISOString(), ...action.payload },
        stats: {
          ...state.stats,
          bsmSessions: state.stats.bsmSessions + 1,
          lastActivity: new Date().toISOString()
        }
      }
    }
    case 'BSM_END': {
      const duration = state.bsm.startedAt 
        ? (new Date().getTime() - new Date(state.bsm.startedAt).getTime()) / 1000
        : 0
      return {
        ...state,
        bsm: { ...initialBSMState },
        stats: {
          ...state.stats,
          totalBSMDuration: state.stats.totalBSMDuration + duration,
          lastActivity: new Date().toISOString()
        }
      }
    }
    case 'BSM_UPDATE': {
      return { ...state, bsm: { ...state.bsm, ...action.payload } }
    }

    // Code Extraction actions
    case 'CODE_EXTRACTED': {
      const existingIndex = state.extractedCode.findIndex(c => c.id === action.payload.id)
      let updatedCode: ExtractedCode[]
      
      if (existingIndex >= 0) {
        updatedCode = [...state.extractedCode]
        updatedCode[existingIndex] = action.payload
      } else {
        updatedCode = [...state.extractedCode, action.payload]
      }
      
      const byLanguage = { ...state.extractionStats.byLanguage }
      const lang = action.payload.language || 'unknown'
      byLanguage[lang] = (byLanguage[lang] || 0) + 1
      
      const bySource = { ...state.extractionStats.bySource }
      const source = action.payload.source || 'unknown'
      bySource[source] = (bySource[source] || 0) + 1
      
      return {
        ...state,
        extractedCode: updatedCode,
        extractionStats: {
          ...state.extractionStats,
          totalExtracted: state.extractionStats.totalExtracted + 1,
          byLanguage,
          bySource,
          lastExtraction: new Date().toISOString(),
        },
        stats: {
          ...state.stats,
          codeSnippetsExtracted: state.stats.codeSnippetsExtracted + 1,
          lastActivity: new Date().toISOString()
        }
      }
    }
    case 'REMOVE_EXTRACTED_CODE': {
      return {
        ...state,
        extractedCode: state.extractedCode.filter(c => c.id !== action.payload)
      }
    }
    case 'CLEAR_EXTRACTED_CODE': {
      return {
        ...state,
        extractedCode: [],
        extractionStats: {
          totalExtracted: 0,
          byLanguage: {},
          bySource: {},
        }
      }
    }

    // Code Optimization actions
    case 'OPTIMIZATION_RESULT': {
      const results = [...state.optimizationResults, action.payload]
      const totalIssues = action.payload.issues.length
      const totalFixes = action.payload.fixesApplied.length
      
      const issuesByType = { ...state.optimizationStats.issuesByType }
      action.payload.issues.forEach(issue => {
        issuesByType[issue.type] = (issuesByType[issue.type] || 0) + 1
      })
      
      return {
        ...state,
        optimizationResults: results,
        optimizationStats: {
          ...state.optimizationStats,
          filesScanned: state.optimizationStats.filesScanned + 1,
          filesWithIssues: totalIssues > 0 
            ? state.optimizationStats.filesWithIssues + 1 
            : state.optimizationStats.filesWithIssues,
          totalIssues: state.optimizationStats.totalIssues + totalIssues,
          issuesByType,
          fixesApplied: state.optimizationStats.fixesApplied + totalFixes,
        },
        stats: {
          ...state.stats,
          issuesFound: state.stats.issuesFound + totalIssues,
          issuesFixed: state.stats.issuesFixed + totalFixes,
          lastActivity: new Date().toISOString()
        }
      }
    }
    case 'CLEAR_OPTIMIZATION_RESULTS': {
      return {
        ...state,
        optimizationResults: [],
        optimizationStats: {
          filesScanned: 0,
          filesWithIssues: 0,
          totalIssues: 0,
          issuesByType: {},
          fixesApplied: 0,
        }
      }
    }

    // Error actions
    case 'LOG_ERROR': {
      return {
        ...state,
        error: action.payload,
        stats: { ...state.stats, lastActivity: new Date().toISOString() }
      }
    }
    case 'CLEAR_ERROR': {
      return { ...state, error: undefined }
    }

    // Settings actions
    case 'SET_API_KEY': {
      return { ...state, settings: { ...state.settings, apiKey: action.payload } }
    }
    case 'TOGGLE_SIMPLE_MODE': {
      const simpleMode = action.payload ?? !state.settings.simpleMode
      return { ...state, settings: { ...state.settings, simpleMode } }
    }
    case 'SET_SETTINGS': {
      return { ...state, settings: { ...state.settings, ...action.payload } }
    }
    case 'SET_PERMISSIONS': {
      return { ...state, permissions: action.payload }
    }

    // UI State actions
    case 'SET_LOADING': {
      return { ...state, isLoading: action.payload }
    }

    // Rehydration
    case 'REHYDRATE': {
      return { ...state, ...action.payload }
    }

    // Reset
    case 'RESET_APP': {
      return { ...initialState, settings: state.settings }
    }

    default:
      return state
  }
}

// ============================================================================
// CONTEXT
// ============================================================================

interface AppContextType {
  state: AppState
  dispatch: React.Dispatch<Action>
}

const AppContext = createContext<AppContextType>({
  state: initialState,
  dispatch: () => null
})

// ============================================================================
// PROVIDER COMPONENT
// ============================================================================

const STORAGE_KEY = 'syntax_ai_captcoder_v1'

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState)

  // Persist state to localStorage
  useEffect(() => {
    const persistState = {
      conversation: state.conversation.slice(-state.settings.maxHistory),
      bsm: state.bsm,
      extractedCode: state.extractedCode.slice(-20),
      settings: state.settings,
      stats: state.stats,
    }
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(persistState))
    } catch (e) {
      console.warn('Failed to persist state:', e)
    }
  }, [state.conversation, state.bsm, state.extractedCode, state.settings, state.stats])

  // Rehydrate state from localStorage
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) {
        const parsed = JSON.parse(raw)
        dispatch({ type: 'REHYDRATE', payload: parsed })
      }
    } catch (e) {
      console.warn('Rehydrate failed:', e)
    }
  }, [])

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  )
}

// ============================================================================
// HOOK
// ============================================================================

export const useAppContext = () => useContext(AppContext)

export { initialState, AppContext, AppProvider, reducer }
export type { AppContextType }
