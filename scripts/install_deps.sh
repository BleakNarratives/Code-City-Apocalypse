#!/bin/bash
set -e
echo "Installing dependencies..."
pkg update -y
pkg install -y ffmpeg sox python python-pip build-essential git nano
pip install --break-system-packages --no-cache-dir pyyaml requests beautifulsoup4 pillow
echo "Installing Google AI (5-10 min)..."
pip install --break-system-packages --no-cache-dir google-generativeai
pip install --break-system-packages --no-cache-dir gtts pydub mido librosa soundfile pedalboard
pip install --break-system-packages --no-cache-dir pandas matplotlib flask
echo "✓ Done! Now run: bash ~/build_code_city.sh"
