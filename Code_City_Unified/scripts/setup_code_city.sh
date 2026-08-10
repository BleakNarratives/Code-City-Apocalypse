#!/bin/bash
# ONE-SHOT CODE CITY SETUP
# Run this and walk away, come back to a complete system

set -e

echo "========================================"
echo "   CODE CITY: ONE-SHOT INSTALL"
echo "   Sit back, this'll take 10-15 min"
echo "========================================"
echo ""

# ============================================
# STEP 1: CHECK DISK SPACE
# ============================================

echo "[1/6] Checking disk space..."
AVAILABLE=$(df /data | tail -1 | awk '{print $4}')
REQUIRED=500000  # 500MB minimum

if [ "$AVAILABLE" -lt "$REQUIRED" ]; then
    echo "⚠️  WARNING: Low disk space ($AVAILABLE KB available)"
    echo "   This might fail. Consider cleaning up first:"
    echo "   pkg clean && pip cache purge"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✓ Disk space OK"

# ============================================
# STEP 2: UPDATE SYSTEM
# ============================================

echo ""
echo "[2/6] Updating system packages..."
pkg update -y
pkg upgrade -y

echo "✓ System updated"

# ============================================
# STEP 3: INSTALL SYSTEM DEPENDENCIES
# ============================================

echo ""
echo "[3/6] Installing system packages..."

# Audio tools
pkg install -y ffmpeg sox

# Python build tools (for heavy packages)
pkg install -y python python-pip build-essential

# Optional but useful
pkg install -y git nano

echo "✓ System packages installed"

# ============================================
# STEP 4: INSTALL PYTHON PACKAGES (THE HEAVY LIFT)
# ============================================

echo ""
echo "[4/6] Installing Python packages..."
echo "    (This is the slow part - grpcio takes ~5-10 min)"
echo "    Go grab coffee, pet the dogs, whatever"
echo ""

# Install in order of dependency complexity
# Start with the simple ones

echo "  → Installing core dependencies..."
pip install --break-system-packages --no-cache-dir \
    pyyaml \
    requests \
    beautifulsoup4 \
    pillow

echo "  → Installing Google AI SDK (grpcio here, be patient)..."
pip install --break-system-packages --no-cache-dir \
    google-generativeai

echo "  → Installing audio libraries..."
pip install --break-system-packages --no-cache-dir \
    gtts \
    pydub \
    mido

echo "  → Installing pro audio tools..."
pip install --break-system-packages --no-cache-dir \
    librosa \
    soundfile \
    pedalboard

echo "  → Installing data/viz libraries..."
pip install --break-system-packages --no-cache-dir \
    pandas \
    matplotlib

echo "  → Installing web framework..."
pip install --break-system-packages --no-cache-dir \
    flask

echo "  → Installing advanced audio (optional, might fail)..."
pip install --break-system-packages --no-cache-dir \
    aubio \
    essentia-tensorflow || echo "⚠️  Some advanced audio libs failed (non-critical)"

echo "✓ Python packages installed"

# ============================================
# STEP 5: CREATE CODE CITY STRUCTURE
# ============================================

echo ""
echo "[5/6] Building Code City structure..."

BASE_DIR="$HOME/code_city"

# Backup existing if present
if [ -d "$BASE_DIR" ]; then
    BACKUP="${BASE_DIR}_backup_$(date +%s)"
    echo "  → Backing up existing Code City to $BACKUP"
    mv "$BASE_DIR" "$BACKUP"
fi

mkdir -p "$BASE_DIR"
cd "$BASE_DIR"


