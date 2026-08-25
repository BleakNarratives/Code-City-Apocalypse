# Save this as ~/syntaxai-weaponized/scripts/setup_project.sh
#!/bin/bash
echo "🚀 Setting up SyntaxAI Weaponized project..."

# Create project root
PROJECT_ROOT="$HOME/syntaxai-weaponized"
mkdir -p "$PROJECT_ROOT"

# Create basic structure
mkdir -p "$PROJECT_ROOT/src/conversation_processor"
mkdir -p "$PROJECT_ROOT/src/clipboard_monitor" 
mkdir -p "$PROJECT_ROOT/src/build_orchestrator"
mkdir -p "$PROJECT_ROOT/tests"
mkdir -p "$PROJECT_ROOT/docs"
mkdir -p "$PROJECT_ROOT/scripts"
mkdir -p "$PROJECT_ROOT/data/raw_conversations"
mkdir -p "$PROJECT_ROOT/data/processed"
mkdir -p "$PROJECT_ROOT/exports/vibe_flow"
mkdir -p "$PROJECT_ROOT/exports/code_blocks"

# Create __init__.py files
touch "$PROJECT_ROOT/src/__init__.py"
touch "$PROJECT_ROOT/src/conversation_processor/__init__.py"
touch "$PROJECT_ROOT/src/clipboard_monitor/__init__.py"
touch "$PROJECT_ROOT/src/build_orchestrator/__init__.py"

echo "✅ Project structure created at: $PROJECT_ROOT"
echo "📁 You can now add your modules to src/"