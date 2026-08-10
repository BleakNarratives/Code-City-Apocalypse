#!/bin/bash
echo "--- 🛠️ MODMIND INFRASTRUCTURE CHECK ---"

# 1. Verify Mistral Key
if [[ $MISTRAL_API_KEY == sk-* ]]; then
    echo "✅ Mistral Key: Detected (Starts with sk-)"
else
    echo "❌ Mistral Key: Missing or invalid format. Please set it."
fi

# 2. Check Chubby Porcupine Party (llama.cpp)
if [ -f ~/llama.cpp/build/bin/llama-cli ]; then
    echo "✅ Engine: Chubby Porcupine Party is BUILT."
else
    echo "❌ Engine: Chubby Porcupine Party NOT FOUND in build dir."
fi

# 3. Check for Gemma Model
if [ -f ~/models/gemma-3.gguf ]; then
    echo "✅ Model: Gemma-3 is in the holster."
else
    echo "❌ Model: ~/models/gemma-3.gguf is missing."
fi

# 4. Fix Vibe Key (Injects whatever is in your current session)
mkdir -p ~/.vibe
echo "MISTRAL_API_KEY=$MISTRAL_API_KEY" > ~/.vibe/.env
echo "✅ Vibe: Config updated with current session key."

echo "---------------------------------------"
