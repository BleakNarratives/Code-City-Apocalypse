#!/bin/bash
ROOT="/storage/ED7B-AD5A/root_2026"

# 1. The Three-Way Sort Districts
OBELISK="$ROOT/The_Obelisk"   # Finished / Truth
LAB="$ROOT/The_Lab"           # Unfinished / Active
STACKS="$ROOT/The_Stacks"     # Other / Bullshit

mkdir -p "$OBELISK" "$LAB" "$STACKS"

# 2. Initial Migration (Based on Audit)
echo "[*] Moving 'github_ready' to The Obelisk..."
[ -d "$ROOT/github_ready" ] && mv "$ROOT/github_ready" "$OBELISK/"

echo "[*] Moving 'context_system' to The Lab (preserving the DNA)..."
[ -d "$ROOT/context_system" ] && mv "$ROOT/context_system" "$LAB/"

echo "[*] Moving '.cache' and 'logs' to The Stacks..."
[ -d "$ROOT/.cache" ] && mv "$ROOT/.cache" "$STACKS/"
[ -d "$ROOT/logs" ] && mv "$ROOT/logs" "$STACKS/"

echo -e "\n[!] The Obelisk has been raised at $OBELISK"
