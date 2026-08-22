#!/bin/bash

# Lean Factory - Single model, crash-proof
termux-wake-lock
echo "🧠 Generating: $@"
ollama run deepseek-coder "Write complete FastAPI project for: $@. Include PostgreSQL, JWT auth, Docker, tests. Output as separate files in ~/root_2026/generated/ with proper directory structure. No explanations."
