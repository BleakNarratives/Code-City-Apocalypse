#!/bin/bash
# Local AI Bridge for TUI
# Uses llama.cpp if available

MODEL_DIR="$HOME/models"
LLAMA_DIR="$HOME/llama.cpp"

# Check for available models
find_model() {
    find "$MODEL_DIR" "$LLAMA_DIR" -name "*.gguf" -o -name "*.bin" 2>/dev/null | head -1
}

MODEL=$(find_model)

if [ -z "$MODEL" ]; then
    echo "No local model found. Please download a model to ~/models/"
    echo "Example: wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    exit 1
fi

echo "Using model: $(basename $MODEL)"
echo "Type your prompt (Ctrl+D to exit):"

while read -p "> " prompt; do
    if [ -z "$prompt" ]; then
        continue
    fi
    
    # Use llama.cpp if available
    if [ -f "$LLAMA_DIR/main" ]; then
        "$LLAMA_DIR/main" -m "$MODEL" -p "$prompt" -n 256 -t 4
    elif [ -f "$LLAMA_DIR/llama-cli" ]; then
        "$LLAMA_DIR/llama-cli" -m "$MODEL" -p "$prompt"
    else
        echo "No llama.cpp binary found. Building..."
        cd ~/llama.cpp && make -j4 && ./main -m "$MODEL" -p "$prompt" -n 256
    fi
    echo ""
done
