import React from 'react'
import { AppProvider } from './context/AppContext'
import { ErrorBoundary } from './components/ErrorBoundary'
import { PermissionsGate } from './components/PermissionsGate'
import { AssistantView } from './components/AssistantView'
import { SettingsView } from './components/SettingsView'
import { CodePreview } from './components/CodePreview'
import { BSMStatusBar } from './components/BSMStatusBar'

/**
 * Main Application Component
 * Syntax AI CaptCoder - Unified code intelligence and extraction system
 */
export default function App() {
  return (
    <AppProvider>
      <ErrorBoundary>
        <PermissionsGate>
          <div className="app-shell">
            {/* Main Content Area */}
            <main className="main">
              <BSMStatusBar />
              <AssistantView />
              <CodePreview />
            </main>
            
            {/* Sidebar */}
            <aside className="aside">
              <SettingsView />
            </aside>
          </div>
        </PermissionsGate>
      </ErrorBoundary>
    </AppProvider>
  )
}
