import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'

// Mount the application
const container = document.getElementById('root')
if (container) {
  createRoot(container).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
} else {
  console.error('Failed to find root element')
}
