/**
 * Strongly-typed interfaces for Syntax AI CaptCoder
 * Unified type system for the entire application
 */

// ============================================================================
// CORE TYPES
// ============================================================================

export type ParticipantRole = 'human' | 'ai' | 'system' | 'CaptCoder' | 'JaneNat';

// Message types for conversation
export interface Message {
  id: string;
  role: ParticipantRole;
  text: string;
  timestamp: string;
  metadata?: MessageMetadata;
}

export interface MessageMetadata {
  language?: string;
  source?: 'chat' | 'voice' | 'screen' | 'file' | 'command';
  codeBlocks?: CodeBlock[];
  tags?: string[];
  confidence?: number; // For AI-generated messages
}

// Code block representation
export interface CodeBlock {
  code: string;
  language: string;
  type: 'fenced' | 'inline' | 'indented';
  lineStart?: number;
  lineEnd?: number;
}

// ============================================================================
// BSM (BLUE SKY MEETING) TYPES
// ============================================================================

export interface BSMState {
  isActive: boolean;
  startedAt?: string;
  endedAt?: string;
  title?: string;
  description?: string;
  livestream?: LivestreamConfig;
  recording?: RecordingConfig;
}

export interface LivestreamConfig {
  provider: string;
  endpoints: string[];
  isLive: boolean;
  streamUrl?: string;
}

export interface RecordingConfig {
  isRecording: boolean;
  filePath?: string;
  durationSeconds: number;
}

// ============================================================================
// CODE EXTRACTION TYPES
// ============================================================================

export interface ExtractedCode {
  id: string;
  source: string;
  code: string;
  language: string;
  timestamp: string;
  filePath?: string;
  lineNumber?: number;
}

export interface ExtractionStats {
  totalExtracted: number;
  byLanguage: Record<string, number>;
  bySource: Record<string, number>;
  lastExtraction?: string;
}

// ============================================================================
// CODE OPTIMIZATION TYPES
// ============================================================================

export interface OptimizationIssue {
  type: 'long_function' | 'missing_docstring' | 'unused_import' | 'print_statement' | 'magic_number' | 'no_type_hint' | 'trailing_whitespace' | 'mixed_indentation' | 'missing_newline';
  severity: 'info' | 'warning' | 'error';
  message: string;
  file: string;
  line?: number;
  column?: number;
  suggestion?: string;
}

export interface OptimizationResult {
  file: string;
  issues: OptimizationIssue[];
  fixesApplied: string[];
  linesChanged: number;
  timestamp: string;
}

export interface OptimizationStats {
  filesScanned: number;
  filesWithIssues: number;
  totalIssues: number;
  issuesByType: Record<string, number>;
  fixesApplied: number;
}

// ============================================================================
// APPLICATION STATE
// ============================================================================

export interface PermissionsState {
  camera: 'granted' | 'denied' | 'prompt' | undefined;
  microphone: 'granted' | 'denied' | 'prompt' | undefined;
  notification: 'granted' | 'denied' | 'prompt' | undefined;
}

export interface SettingsState {
  simpleMode: boolean;
  apiKey?: string | null;
  theme: 'light' | 'dark' | 'system';
  enableTTS: boolean;
  enableSound: boolean;
  maxHistory: number;
  autoOptimize: boolean;
  watchDirectories: string[];
}

export interface AppState {
  // Conversation
  conversation: Message[];
  
  // BSM State
  bsm: BSMState;
  
  // Code Extraction
  extractedCode: ExtractedCode[];
  extractionStats: ExtractionStats;
  
  // Code Optimization
  optimizationResults: OptimizationResult[];
  optimizationStats: OptimizationStats;
  
  // UI State
  isLoading: boolean;
  error?: AppError;
  
  // Settings
  permissions: PermissionsState;
  settings: SettingsState;
  
  // Statistics
  stats: AppStatistics;
}

// ============================================================================
// ERROR HANDLING
// ============================================================================

export interface AppError {
  id: string;
  code: string;
  message: string;
  details?: any;
  timestamp: string;
  severity: 'info' | 'warning' | 'error' | 'critical';
}

// ============================================================================
// STATISTICS & METRICS
// ============================================================================

export interface AppStatistics {
  // BSM
  bsmSessions: number;
  totalBSMDuration: number;
  
  // Code Extraction
  codeSnippetsExtracted: number;
  filesMonitored: number;
  
  // Code Optimization
  issuesFound: number;
  issuesFixed: number;
  
  // Commands
  commandsProcessed: number;
  nexusRequests: number;
  
  // General
  appStartTime: string;
  lastActivity: string;
}

// ============================================================================
// CONTEXT MANAGEMENT (from original)
// ============================================================================

export interface DeviceSpec {
  vendor?: string;
  model?: string;
  codename?: string;
  soc?: string;
  storage?: 'eMMC' | 'UFS' | 'UNKNOWN';
  bootloader?: 'locked' | 'unlocked' | 'unknown';
  usb_debugging?: boolean | 'unknown';
  power_state?: 'battery' | 'charging' | 'unknown';
}

export interface RecoveryAction {
  id: string;
  title: string;
  description: string;
  risk: 'low' | 'medium' | 'high';
  prerequisites?: string[];
  tools?: string[];
  vendor_constraints?: string[];
}

export interface HardwareRecovery {
  emmc_extraction?: {
    tools: string[];
    temperature_range_c: { min: number; max: number };
    airflow_cfm?: number;
    nozzle_distance_mm?: { min: number; max: number };
    timing_seconds?: { min: number; max: number };
    notes?: string;
  };
  ram_preservation?: {
    maintain_power: boolean;
    window_seconds?: number;
    notes?: string;
  };
}

export interface ConversationContext {
  bootstrap_metadata?: {
    version?: string;
    timestamp?: string;
    protocol_name?: string;
    purpose?: string;
  };
  conversation_context?: {
    core_project?: string;
    project_status?: string;
    current_phase?: string;
    human?: {
      name?: string;
      approach?: string;
      philosophy?: string;
      projects?: string[];
    };
    technical_elements?: {
      hardware_recovery?: HardwareRecovery;
      software_exploits?: {
        bootloader_modes?: string[];
        tools?: string[];
      };
      context_preservation?: {
        json_bootstrap_handoff?: string;
        proto_schema_buffer?: string;
      };
    };
    key_insights?: {
      problem_identification?: { real_issue?: string; actual_truth?: string };
      next_steps?: { immediate?: string[]; technical?: string[] };
    };
  };
  [k: string]: any;
}

// ============================================================================
// NEXUS API TYPES
// ============================================================================

export interface NexusCommand {
  raw_input: string;
  source_agent: string;
  timestamp?: string;
  metadata?: Record<string, any>;
}

export interface NexusResponse {
  status: 'queued' | 'processing' | 'completed' | 'error';
  action?: string;
  result?: any;
  error?: string;
  request_id: string;
  timestamp: string;
}

// ============================================================================
// SANDBOX & LOOKING GLASS TYPES
// ============================================================================

export interface SandboxTest {
  id: string;
  code: string;
  language: string;
  status: 'queued' | 'running' | 'passed' | 'failed' | 'error';
  output?: string;
  error?: string;
  duration?: number;
  timestamp: string;
}

export interface LookingGlassPreview {
  variables: Record<string, any>;
  uiElements: any[];
  screenshot?: string; // base64 encoded
  timestamp: string;
}

// ============================================================================
// ACTION TYPES
// ============================================================================

export type AppAction =
  // Conversation actions
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'UPDATE_MESSAGE'; payload: { id: string; updates: Partial<Message> } }
  | { type: 'REMOVE_MESSAGE'; payload: string }
  | { type: 'CLEAR_CONVERSATION' }
  
  // BSM actions
  | { type: 'BSM_START'; payload?: Partial<BSMState> }
  | { type: 'BSM_END' }
  | { type: 'BSM_UPDATE'; payload: Partial<BSMState> }
  
  // Code Extraction actions
  | { type: 'CODE_EXTRACTED'; payload: ExtractedCode }
  | { type: 'REMOVE_EXTRACTED_CODE'; payload: string }
  | { type: 'CLEAR_EXTRACTED_CODE' }
  
  // Code Optimization actions
  | { type: 'OPTIMIZATION_RESULT'; payload: OptimizationResult }
  | { type: 'CLEAR_OPTIMIZATION_RESULTS' }
  
  // Error actions
  | { type: 'LOG_ERROR'; payload: AppError }
  | { type: 'CLEAR_ERROR' }
  
  // Settings actions
  | { type: 'SET_API_KEY'; payload: string | null }
  | { type: 'TOGGLE_SIMPLE_MODE'; payload?: boolean }
  | { type: 'SET_SETTINGS'; payload: Partial<SettingsState> }
  | { type: 'SET_PERMISSIONS'; payload: PermissionsState }
  
  // UI State actions
  | { type: 'SET_LOADING'; payload: boolean }
  
  // Rehydration
  | { type: 'REHYDRATE'; payload: Partial<Omit<AppState, 'isLoading' | 'error'>> }
  
  // Reset
  | { type: 'RESET_APP' };
