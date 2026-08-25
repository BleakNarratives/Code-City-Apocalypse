/**
 * Context Manager for Syntax AI CaptCoder
 * Manages and queries the conversation context
 * Integrated from phase_1_v_2/src/services/contextManager.ts
 */

import type { ConversationContext } from '../types'

// Default context - can be loaded from a JSON file
let context: ConversationContext = {
  bootstrap_metadata: {
    version: '1.0',
    timestamp: new Date().toISOString(),
    protocol_name: 'Syntax_AI_CaptCoder',
    purpose: 'Unified code intelligence and extraction system',
  },
  conversation_context: {
    core_project: 'syntax_ai_captcoder',
    project_status: 'active_development',
    current_phase: 'unification',
    human: {
      name: 'user',
      approach: 'code_creator',
      philosophy: 'build_with_ai_assistance',
      projects: ['ModMind', 'EquiLex', 'Syntax AI', 'ShipWrekD'],
    },
    technical_elements: {
      hardware_recovery: {},
      software_exploits: {
        bootloader_modes: ['development', 'debug', 'production'],
        tools: ['syntax_ai', 'captcoder', 'nexus'],
      },
      context_preservation: {
        json_bootstrap_handoff: 'enabled',
        proto_schema_buffer: 'enabled',
      },
    },
    key_insights: {
      problem_identification: {
        real_issue: 'code_intelligence_unification',
        actual_truth: 'consolidating_all_code_extraction_and_optimization_tools',
      },
      next_steps: {
        immediate: ['complete_typeScript_ui_migration', 'create_service_modules'],
        technical: ['integrate_all_loosies_code', 'test_all_components', 'deploy_to_production'],
      },
    },
  },
}

/**
 * Snippet for context indexing
 */
interface Snippet {
  path: string
  text: string
  score?: number
}

/**
 * Extract snippets from context recursively
 */
function extractSnippets(ctx: any, prefix: string = ''): Snippet[] {
  const out: Snippet[] = []
  
  if (typeof ctx === 'string' || typeof ctx === 'number' || typeof ctx === 'boolean') {
    out.push({ path: prefix, text: String(ctx) })
    return out
  }
  
  if (Array.isArray(ctx)) {
    ctx.forEach((v, i) => out.push(...extractSnippets(v, `${prefix}[${i}]`)))
    return out
  }
  
  Object.keys(ctx).forEach(k => {
    const v = (ctx as Record<string, any>)[k]
    const path = prefix ? `${prefix}.${k}` : k
    if (typeof v === 'string' && v.length < 1200) {
      out.push({ path, text: v })
    } else if (typeof v === 'object' && v !== null) {
      out.push(...extractSnippets(v, path))
    }
  })
  
  return out
}

/**
 * Get all snippets from context
 */
function getAllSnippets(): Snippet[] {
  return extractSnippets(context)
}

/**
 * Score a snippet by keyword hits
 */
function scoreSnippet(snippet: Snippet, tokens: string[]): number {
  const low = snippet.text.toLowerCase()
  let score = 0
  
  tokens.forEach(t => {
    if (!t) return
    const re = new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')
    const m = low.match(re)
    if (m) score += m.length
  })
  
  return score
}

/**
 * Query the context with a user query
 * Returns relevant snippets with provenance
 */
export function queryContext(query: string, maxTokens: number = 800): { contextString: string; sources: string[] } {
  const tokens = query.toLowerCase().split(/\W+/).filter(Boolean).slice(0, 30)
  const scored = getAllSnippets().map(s => ({ ...s, score: scoreSnippet(s, tokens) }))
  
  scored.sort((a, b) => (b.score || 0) - (a.score || 0))
  
  const selected: Snippet[] = []
  const sources: string[] = []
  let length = 0
  
  for (const s of scored) {
    if (!s.score || s.score <= 0) break
    const addLen = s.text.length
    if (length + addLen > maxTokens) continue
    selected.push(s)
    sources.push(s.path)
    length += addLen
    if (selected.length >= 10) break
  }
  
  const contextString = selected.map(s => `[${s.path}] ${s.text}`).join('\n---\n')
  
  return { contextString, sources }
}

/**
 * Get raw context
 */
export function getRawContext(): ConversationContext {
  return context
}

/**
 * Set context (for initialization or updates)
 */
export function setContext(newContext: ConversationContext): void {
  context = newContext
}

/**
 * Update context
 */
export function updateContext(updates: Partial<ConversationContext>): void {
  context = { ...context, ...updates }
}

/**
 * Clear context
 */
export function clearContext(): void {
  context = {
    bootstrap_metadata: {
      version: '1.0',
      timestamp: new Date().toISOString(),
      protocol_name: 'Syntax_AI_CaptCoder',
      purpose: 'Unified code intelligence and extraction system',
    },
    conversation_context: {},
  }
}

/**
 * Search context for specific keys
 */
export function searchContext(searchTerm: string): any[] {
  const results: any[] = []
  
  function searchInObject(obj: any, path: string = ''): void {
    if (typeof obj === 'object' && obj !== null) {
      Object.keys(obj).forEach(k => {
        const value = obj[k]
        const currentPath = path ? `${path}.${k}` : k
        
        if (typeof value === 'string' && value.toLowerCase().includes(searchTerm.toLowerCase())) {
          results.push({ path: currentPath, value })
        } else if (typeof value === 'object' && value !== null) {
          searchInObject(value, currentPath)
        }
      })
    }
  }
  
  searchInObject(context)
  return results
}

export default {
  queryContext,
  getRawContext,
  setContext,
  updateContext,
  clearContext,
  searchContext,
}
