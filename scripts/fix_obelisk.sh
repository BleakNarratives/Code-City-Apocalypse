#!/bin/bash
ROOT="/storage/ED7B-AD5A/root_2026"

# 1. Force the creation of the Districts now that space is clear
mkdir -p "$ROOT/The_Obelisk" "$ROOT/The_Lab" "$ROOT/The_Stacks"

# 2. Rename/Move existing high-value folders safely
echo "[*] Raising The Obelisk..."
[ -d "$ROOT/github_ready" ] && mv "$ROOT/github_ready"/* "$ROOT/The_Obelisk/" 2>/dev/null

echo "[*] Placing DNA in The Lab..."
[ -d "$ROOT/context_system" ] && mv "$ROOT/context_system" "$ROOT/The_Lab/" 2>/dev/null

echo "[*] Sorting standard bullshit into The Stacks..."
[ -d "$ROOT/logs" ] && mv "$ROOT/logs" "$ROOT/The_Stacks/" 2>/dev/null

# 3. Final cleanup of the 'ghost' folders
find "$ROOT" -type d -empty -delete

echo -e "\n[!] The Obelisk is stable. Storage has been reclaimed."
