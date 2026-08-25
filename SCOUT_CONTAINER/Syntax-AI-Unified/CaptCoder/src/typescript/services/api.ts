/**
 * API Service for Syntax AI CaptCoder
 * Handles communication with the backend Nexus API
 */

import type { Message, NexusCommand, NexusResponse, ExtractedCode } from '../types'

// Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const NEXUS_COMMAND_URL = `${API_BASE_URL}/command`

/**
 * Call the Nexus API with a command
 */
export async function callNexus(command: NexusCommand): Promise<NexusResponse> {
  try {
    const response = await fetch(NEXUS_COMMAND_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(command),
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`Nexus API error ${response.status}: ${errorText}`)
    }

    return await response.json()
  } catch (error) {
    return {
      status: 'error',
      action: 'nexus_call_failed',
      error: error instanceof Error ? error.message : String(error),
      request_id: Date.now().toString(),
      timestamp: new Date().toISOString(),
    }
  }
}

/**
 * Send a message for processing
 */
export async function sendMessage(message: string, apiKey?: string): Promise<{ ok: boolean; reply?: string; error?: string }> {
  const command: NexusCommand = {
    raw_input: message,
    source_agent: 'CaptCoder-Web',
    timestamp: new Date().toISOString(),
  }

  if (apiKey) {
    // If we have a direct API key, we could use it here
    // For now, we'll use the Nexus API
  }

  const response = await callNexus(command)

  if (response.status === 'error') {
    return {
      ok: false,
      error: response.error || 'Nexus API error',
    }
  }

  // Extract reply from response
  const reply = response.result?.reply || response.result || 'Request processed'

  return {
    ok: true,
    reply,
  }
}

/**
 * Extract code from text
 */
export async function extractCode(text: string, apiKey?: string): Promise<{ ok: boolean; code?: ExtractedCode; error?: string }> {
  const command: NexusCommand = {
    raw_input: text,
    source_agent: 'CaptCoder-Web',
    timestamp: new Date().toISOString(),
    metadata: {
      action: 'extract_code',
    },
  }

  const response = await callNexus(command)

  if (response.status === 'error') {
    return {
      ok: false,
      error: response.error || 'Failed to extract code',
    }
  }

  // Extract code from response
  const codeData = response.result?.code || response.result

  if (!codeData) {
    return {
      ok: false,
      error: 'No code found in response',
    }
  }

  // Create ExtractedCode object
  const extractedCode: ExtractedCode = {
    id: `code_${Date.now()}`,
    source: 'web',
    code: codeData.code || codeData,
    language: codeData.language || 'unknown',
    timestamp: new Date().toISOString(),
  }

  return {
    ok: true,
    code: extractedCode,
  }
}

/**
 * Start a Blue Sky Meeting
 */
export async function startBSM(title: string, description?: string): Promise<{ ok: boolean; error?: string }> {
  const command: NexusCommand = {
    raw_input: `#bsm ${title}${description ? ': ' + description : ''}`,
    source_agent: 'CaptCoder-Web',
    timestamp: new Date().toISOString(),
    metadata: {
      action: 'bsm_start',
      title,
      description,
    },
  }

  const response = await callNexus(command)

  if (response.status === 'error') {
    return {
      ok: false,
      error: response.error || 'Failed to start BSM',
    }
  }

  return { ok: true }
}

/**
 * End a Blue Sky Meeting
 */
export async function endBSM(): Promise<{ ok: boolean; error?: string }> {
  const command: NexusCommand = {
    raw_input: '#bsm-end',
    source_agent: 'CaptCoder-Web',
    timestamp: new Date().toISOString(),
    metadata: {
      action: 'bsm_end',
    },
  }

  const response = await callNexus(command)

  if (response.status === 'error') {
    return {
      ok: false,
      error: response.error || 'Failed to end BSM',
    }
  }

  return { ok: true }
}

/**
 * Get health status of the backend
 */
export async function checkHealth(): Promise<{ ok: boolean; status?: string; error?: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    
    if (!response.ok) {
      return {
        ok: false,
        error: `Health check failed with status ${response.status}`,
      }
    }

    const data = await response.json()
    return {
      ok: true,
      status: data.status || 'healthy',
    }
  } catch (error) {
    return {
      ok: false,
      error: error instanceof Error ? error.message : String(error),
    }
  }
}

/**
 * Generate code from natural language description
 */
export async function generateCode(description: string, language: string = 'python'): Promise<{ ok: boolean; code?: string; error?: string }> {
  const command: NexusCommand = {
    raw_input: `#${language} ${description}`,
    source_agent: 'CaptCoder-Web',
    timestamp: new Date().toISOString(),
    metadata: {
      action: 'generate_code',
      language,
    },
  }

  const response = await callNexus(command)

  if (response.status === 'error') {
    return {
      ok: false,
      error: response.error || 'Failed to generate code',
    }
  }

  const code = response.result?.code || response.result

  if (!code) {
    return {
      ok: false,
      error: 'No code generated',
    }
  }

  return {
    ok: true,
    code: typeof code === 'string' ? code : JSON.stringify(code),
  }
}

export default {
  callNexus,
  sendMessage,
  extractCode,
  startBSM,
  endBSM,
  checkHealth,
  generateCode,
}
