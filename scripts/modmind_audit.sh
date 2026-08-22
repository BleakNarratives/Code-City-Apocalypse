#!/bin/bash
# Using absolute HOME path to avoid the tilde error
REPORT="$HOME/modmind_audit.txt"
echo "MODMIND / EQUINEX - ARCHITECTURAL AUDIT" > "$REPORT"
echo "Generated: $(date)" >> "$REPORT"
echo "----------------------------------------" >> "$REPORT"

echo -e "\n[DISTRICT: YOU-ARE-HERE]" >> "$REPORT"
ls -R ~/YOU-ARE-HERE 2>/dev/null >> "$REPORT"

echo -e "\n[DISTRICT: OTHER (SD)]" >> "$REPORT"
ls -R ~/home/other 2>/dev/null >> "$REPORT"

echo -e "\n[INFRASTRUCTURE: LOOP DETECTION]" >> "$REPORT"
find $HOME  ~/ -maxdepth 10 -type d 2>/dev/null | awk -F'/' 'NF > 8' >> "$REPORT"

echo -e "\n[DISTRICT: SNAPSHOTS]" >> "$REPORT"
echo "Total File Count: $(find ~/snapshots -type f 2>/dev/null | wc -l)" >> "$REPORT"
ls -F ~/snapshots 2>/dev/null | head -n 20 >> "$REPORT"

echo -e "\n[LOGISTICS: THE THREE-WAY SORT]" >> "$REPORT"
find ~/ -maxdepth 2 -type d 2>/dev/null >> "$REPORT"

echo -e "\nAudit Complete. File saved at: $REPORT"
