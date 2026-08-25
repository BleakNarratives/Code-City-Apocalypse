import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
      '@components': path.resolve(__dirname, './components'),
      '@contexts': path.resolve(__dirname, './contexts'),
      '@services': path.resolve(__dirname, './services'),
      '@utils': path.resolve(__dirname, './utils'),
    },
  },
  server: {
    port: 5173,
    host: true,
  },
  build: {
    outDir: '../../dist/typescript',
    emptyOutDir: true,
  },
})
