// Syntax AI CaptCoder - TypeScript Entry Point
// Export all public API

// Components
export { AssistantView } from './components/AssistantView'
export { CodePreview } from './components/CodePreview'
export { ErrorBoundary } from './components/ErrorBoundary'
export { PermissionsGate } from './components/PermissionsGate'
export { SettingsView } from './components/SettingsView'
export { BSMStatusBar } from './components/BSMStatusBar'

// Context
export { AppProvider, useAppContext, AppContext, initialState, reducer } from './context/AppContext'

// Services
export { callNexus, sendMessage, extractCode, startBSM, endBSM, checkHealth, generateCode } from './services/api'
export { queryContext, getRawContext, setContext, updateContext, clearContext, searchContext } from './services/contextManager'

// Utils
export { formatError, useHandleError, createError, logError, isError } from './utils/handleError'

// Types
export type {
  ParticipantRole,
  Message,
  MessageMetadata,
  CodeBlock,
  BSMState,
  LivestreamConfig,
  RecordingConfig,
  ExtractedCode,
  ExtractionStats,
  OptimizationIssue,
  OptimizationResult,
  OptimizationStats,
  PermissionsState,
  SettingsState,
  AppState,
  AppError,
  AppStatistics,
  DeviceSpec,
  RecoveryAction,
  HardwareRecovery,
  ConversationContext,
  NexusCommand,
  NexusResponse,
  SandboxTest,
  LookingGlassPreview,
  AppAction,
} from './types'
