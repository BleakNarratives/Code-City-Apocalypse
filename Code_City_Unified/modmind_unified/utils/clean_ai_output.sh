#!/data/data/com.termux/files/usr/bin/bash
# Description: Cleans AI output by removing conversational fluff, extracting only code blocks.
# Usage:
#   echo "AI output with ```code``` and fluff" | ./clean_ai_output.sh
#   ./clean_ai_output.sh < ai_output.txt
#   ./clean_ai_output.sh input.txt > output.txt

# Ensure pull_patterns.sh exists and is executable
if [ ! -f "$HOME/pull_patterns.sh" ]; then
    echo "Error: ~/pull_patterns.sh not found!" >&2
    exit 1
fi
if [ ! -x "$HOME/pull_patterns.sh" ]; then
    echo "Error: ~/pull_patterns.sh is not executable!" >&2
    exit 1
fi

# Use pull_patterns.sh to extract code blocks
"$HOME/pull_patterns.sh" "$@"
