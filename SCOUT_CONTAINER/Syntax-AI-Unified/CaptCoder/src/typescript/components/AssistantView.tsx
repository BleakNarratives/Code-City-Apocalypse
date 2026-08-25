import React, { useState, useRef, useEffect } from 'react'
import { useAppContext } from '../context/AppContext'
import type { Message } from '../types'

/**
 * Assistant View Component
 * Main conversation interface for Syntax AI CaptCoder
 */
export const AssistantView: React.FC = () => {
  const { state, dispatch } = useAppContext()
  const [text, setText] = useState('')
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [state.conversation])

  // Handle sending message
  const send = async () => {
    if (!text.trim() || isSending) return
    
    setIsSending(true)
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'human',
      text: text.trim(),
      timestamp: new Date().toISOString(),
      metadata: {
        source: 'chat',
        language: detectLanguage(text),
      }
    }
    
    dispatch({ type: 'ADD_MESSAGE', payload: userMessage })
    setText('')
    
    // Simulate assistant response (replace with actual AI call)
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      text: 'Processing your request... (Syntax AI CaptCoder is analyzing)',
      timestamp: new Date().toISOString(),
      metadata: { source: 'ai' }
    }
    dispatch({ type: 'ADD_MESSAGE', payload: assistantMessage })
    
    // TODO: Replace with actual Nexus API call
    try {
      // Send to Nexus API
      const response = await fetch('/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          raw_input: text,
          source_agent: 'CaptCoder-Web',
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        // Update last message with actual response
        dispatch({
          type: 'UPDATE_MESSAGE',
          payload: {
            id: assistantMessage.id,
            updates: { 
              text: data.result?.reply || 'Request processed by Syntax AI',
              metadata: { ...assistantMessage.metadata, confidence: data.confidence }
            }
          }
        })
      }
    } catch (e) {
      dispatch({
        type: 'UPDATE_MESSAGE',
        payload: {
          id: assistantMessage.id,
          updates: { 
            text: 'Error: Could not connect to Syntax AI. Please check your connection.'
          }
        }
      })
      dispatch({
        type: 'LOG_ERROR',
        payload: {
          id: Date.now().toString(),
          code: 'NEXUS_CONNECTION_FAILED',
          message: 'Failed to connect to Nexus API',
          details: e,
          timestamp: new Date().toISOString(),
          severity: 'error'
        }
      })
    } finally {
      setIsSending(false)
    }
  }

  // Detect language from text
  const detectLanguage = (text: string): string | undefined => {
    const patterns: Record<string, RegExp[]> = {
      python: [/def /, /import /, /class /, /print\(/, /self\./],
      javascript: [/function /, /const /, /let /, /=>/, /console\.log/],
      typescript: [/interface /, /type /, /any /, /number /],
      java: [/public /, /private /, /class /, /void /],
      bash: [/#!\/bin\/bash/, /echo /, /grep /, /sed /],
      html: [/<!DOCTYPE/, /<html/, /<body/, /<div/],
      css: [/^\s*\{/, /class /, /id /, /@media/],
    }
    
    for (const [lang, regexes] of Object.entries(patterns)) {
      for (const regex of regexes) {
        if (regex.test(text)) return lang
      }
    }
    return undefined
  }

  // Handle key down
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  // Handle BSM command
  const handleBSMCommand = (text: string) => {
    if (text.includes('#bsm')) {
      dispatch({
        type: 'BSM_START',
        payload: {
          title: 'Blue Sky Meeting',
          description: text.replace('#bsm', '').trim() || 'Live coding session'
        }
      })
      
      dispatch({
        type: 'ADD_MESSAGE',
        payload: {
          id: Date.now().toString(),
          role: 'system',
          text: '🚀 Blue Sky Meeting started! Code extraction and monitoring active.',
          timestamp: new Date().toISOString(),
          metadata: { source: 'bsm' }
        }
      })
    }
    
    if (text.includes('#bsm-end') || text.toLowerCase().includes('end blue sky meeting')) {
      dispatch({ type: 'BSM_END' })
      dispatch({
        type: 'ADD_MESSAGE',
        payload: {
          id: Date.now().toString(),
          role: 'system',
          text: '🛑 Blue Sky Meeting ended. Session summary saved.',
          timestamp: new Date().toISOString(),
          metadata: { source: 'bsm' }
        }
      })
    }
  }

  // Check for BSM commands in input
  useEffect(() => {
    if (text.includes('#bsm') || text.toLowerCase().includes('#bsm-end') || text.toLowerCase().includes('end blue sky meeting')) {
      handleBSMCommand(text)
    }
  }, [text])

  return (
    <div className="card" style={{ marginBottom: 24 }}>
      <div className="syntax-ai-header" style={{ marginBottom: 0 }}>
        <div className="syntax-ai-logo">SA</div>
        <div className="syntax-ai-title">Syntax AI CaptCoder</div>
      </div>
      
      <p style={{ color: '#64748b', fontSize: 14, marginBottom: 16 }}>
        Enter code or commands. Use <code>#bsm</code> to start a Blue Sky Meeting.
      </p>

      {/* Conversation area */}
      <div style={{
        border: '1px solid var(--border)',
        borderRadius: 8,
        padding: 16,
        minHeight: 300,
        maxHeight: 500,
        overflowY: 'auto',
        background: '#fff',
        marginBottom: 16
      }}>
        {state.conversation.length === 0 ? (
          <div style={{ color: '#94a3b8', textAlign: 'center', padding: 24 }}>
            <p>🎤 Say something or paste code to begin.</p>
            <p style={{ fontSize: 13, marginTop: 8 }}>
              Try: "JaneNat, create a Python class" or paste code with backticks
            </p>
          </div>
        ) : (
          state.conversation.map((message, index) => (
            <div 
              key={message.id} 
              style={{
                marginBottom: 12,
                display: 'flex',
                gap: 8,
                alignItems: 'flex-start'
              }}
            >
              {/* Avatar/Role indicator */}
              <div style={{
                width: 28,
                height: 28,
                borderRadius: 14,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 12,
                fontWeight: 600,
                flexShrink: 0,
                background: getRoleColor(message.role)
              }}>
                {getRoleInitial(message.role)}
              </div>
              
              {/* Message content */}
              <div style={{
                maxWidth: '80%',
                background: getMessageBackground(message.role),
                padding: 12,
                borderRadius: 12,
                fontSize: 14,
                lineHeight: 1.5
              }}>
                {formatMessage(message.text)}
                {message.metadata?.codeBlocks?.length && (
                  <div style={{ marginTop: 8 }}>
                    {message.metadata.codeBlocks.map((block, i) => (
                      <pre key={i} style={{ marginTop: 8, fontSize: 12 }}>
                        <code>{block.code}</code>
                      </pre>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          className="input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Paste code or type a command (e.g., 'JaneNat, create a class')..."
          disabled={isSending}
          style={{ flex: 1 }}
        />
        <button
          className="btn"
          onClick={send}
          disabled={!text.trim() || isSending}
        >
          {isSending ? <span className="spinner" style={{ width: 16, height: 16 }} /> : 'Send'}
        </button>
      </div>
      
      {/* Quick actions */}
      <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <button 
          className="btn-outline" 
          onClick={() => {
            const bsmText = '#bsm Start Blue Sky Meeting for live coding'
            setText(bsmText)
          }}
          title="Start BSM"
        >
          #bsm
        </button>
        <button 
          className="btn-outline" 
          onClick={() => {
            const codeText = '```python\nclass Example:\n    pass\n```'
            setText(codeText)
          }}
          title="Insert Python code block"
        >
          Python Code
        </button>
        <button 
          className="btn-outline" 
          onClick={() => {
            const command = 'JaneNat, generate React component'
            setText(command)
          }}
          title="JaneNat command"
        >
          JaneNat
        </button>
        <button 
          className="btn-outline" 
          onClick={() => dispatch({ type: 'CLEAR_CONVERSATION' })}
          title="Clear conversation"
        >
          Clear
        </button>
      </div>
    </div>
  )
}

// Helper functions
function getRoleColor(role: string): string {
  const colors: Record<string, string> = {
    human: '#3b82f6',
    assistant: '#8b5cf6',
    system: '#6b7280',
    CaptCoder: '#10b981',
    JaneNat: '#f59e0b',
  }
  return colors[role] || '#9ca3af'
}

function getRoleInitial(role: string): string {
  const initials: Record<string, string> = {
    human: '👤',
    assistant: '🤖',
    system: '⚙️',
    CaptCoder: 'C',
    JaneNat: 'J',
  }
  return initials[role] || role.charAt(0).toUpperCase()
}

function getMessageBackground(role: string): string {
  const backgrounds: Record<string, string> = {
    human: '#f1f5f9',
    assistant: '#e0f2fe',
    system: '#fef3c7',
    CaptCoder: '#d1fae5',
    JaneNat: '#fef3c7',
  }
  return backgrounds[role] || '#fff'
}

function formatMessage(text: string): React.ReactNode {
  // Format code blocks
  const codeBlockPattern = /```(\w*)\n?([\s\S]*?)```/g
  const inlineCodePattern = /`([^`]+)`/g
  
  let result: React.ReactNode = text
  
  // Process code blocks
  result = text.replace(codeBlockPattern, (match, lang, code) => (
    <pre key={Math.random()} style={{ margin: '8px 0', background: '#1e293b', padding: 12, borderRadius: 6, overflowX: 'auto' }}>
      <code style={{ color: '#e2e8f0', fontFamily: 'monospace' }}>{code.trim()}</code>
    </pre>
  ))
  
  // Process inline code
  result = result.replace(inlineCodePattern, (match, code) => (
    <code key={Math.random()} style={{ background: '#f1f5f9', padding: '2px 4px', borderRadius: 4, fontFamily: 'monospace' }}>
      {code}
    </code>
  ))
  
  return result
}

export default AssistantView
