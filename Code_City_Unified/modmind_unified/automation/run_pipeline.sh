#!/bin/bash
# run_pipeline.sh - Full Scrape → Analyze → Pitch Pipeline
# One command runs everything end to end
#
# Usage:
#   ./run_pipeline.sh                          (interactive menu)
#   ./run_pipeline.sh "plumbers wichita kansas" (direct query, runs all)
#   ./run_pipeline.sh --cached                 (run on last scraped data)
#   ./run_pipeline.sh --skip-ai "query"        (keyword extraction only, no Ollama needed)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOME_DIR="$HOME"
SCRAPER="$HOME_DIR/modmind_unified/automation/scraper.py"
PAIN_ENGINE="$HOME_DIR/modmind_unified/automation/pain_engine.py"
PYTCH="$HOME_DIR/modmind_unified/pytch_ai_interface.py"
CACHE_DIR="$HOME_DIR/modmind_unified/automation/cache"
PAIN_DIR="$HOME_DIR/modmind_unified/automation/pain_points"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------------------------

banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════╗"
    echo "║     VERTICAL AI - PAIN POINT PIPELINE     ║"
    echo "║  Scrape → Extract → Pattern → Pitch       ║"
    echo "╚═══════════════════════════════════════════╝"
    echo -e "${NC}"
}

progress() {
    echo -e "${GREEN}[✓]${NC} $1"
}

step() {
    echo -e "${YELLOW}[→]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
}

# ---------------------------------------------------------------------------
# PIPELINE STAGES
# ---------------------------------------------------------------------------

run_scraper() {
    local query="$1"
    local skip_ai="$2"
    
    step "STAGE 1: Scraping reviews..."
    
    SCRAPE_OUTPUT=$(python3 "$SCRAPER" --source all --query "$query" 2>&1)
    echo "$SCRAPE_OUTPUT"
    
    # Extract the output file path from scraper output
    SCRAPED_FILE=$(echo "$SCRAPE_OUTPUT" | grep "\[SAVED\]" | sed 's/.*\[SAVED\] //')
    
    if [ -z "$SCRAPED_FILE" ] || [ ! -f "$SCRAPED_FILE" ]; then
        error "Scraper didn't produce output file"
        return 1
    fi
    
    progress "Scraper complete: $SCRAPED_FILE"
    return 0
}

run_pain_engine() {
    local input_file="$1"
    local skip_ai="$2"
    
    step "STAGE 2: Extracting pain points & patterns..."
    
    local skip_flag=""
    if [ "$skip_ai" = "true" ]; then
        skip_flag="--skip-ai"
        echo -e "${YELLOW}  (using keyword extraction - no Ollama)${NC}"
    else
        # Check if Ollama is running
        if ! curl -s http://localhost:11434/api/tags --max-time 3 > /dev/null 2>&1; then
            step "Ollama not running. Starting..."
            ollama serve &
            sleep 3
        fi
    fi
    
    PAIN_OUTPUT=$(python3 "$PAIN_ENGINE" --input "$input_file" $skip_flag 2>&1)
    echo "$PAIN_OUTPUT"
    
    # Extract pytch file path
    PYTCH_FILE=$(echo "$PAIN_OUTPUT" | grep "Pytch input:" | sed 's/.*Pytch input:  //')
    DNA_FILE=$(echo "$PAIN_OUTPUT" | grep "DNA pattern:" | sed 's/.*DNA pattern:  //')
    
    if [ -z "$PYTCH_FILE" ] || [ ! -f "$PYTCH_FILE" ]; then
        error "Pain engine didn't produce pytch output"
        return 1
    fi
    
    progress "Pain engine complete"
    progress "Pytch input: $PYTCH_FILE"
    [ -n "$DNA_FILE" ] && progress "DNA pattern: $DNA_FILE"
    return 0
}

run_pytch() {
    local input_file="$1"
    
    step "STAGE 3: Generating pitch output..."
    
    PYTCH_OUTPUT=$(python3 "$PYTCH" "$input_file" 2>&1)
    echo "$PYTCH_OUTPUT"
    
    # Save pytch output
    local outfile="$PAIN_DIR/pitch_$(date +%s).json"
    echo "$PYTCH_OUTPUT" > "$outfile"
    
    progress "Pitch generated: $outfile"
    return 0
}

# ---------------------------------------------------------------------------
# FULL PIPELINE
# ---------------------------------------------------------------------------

run_full_pipeline() {
    local query="$1"
    local skip_ai="$2"
    
    banner
    echo -e "${CYAN}Query: ${NC}$query"
    echo -e "${CYAN}AI Mode: ${NC}$([ "$skip_ai" = "true" ] && echo "keyword-only" || echo "Ollama-powered")"
    echo ""
    
    # Stage 1: Scrape
    run_scraper "$query" "$skip_ai"
    if [ $? -ne 0 ]; then
        error "Pipeline failed at scraping stage"
        return 1
    fi
    echo ""
    
    # Stage 2: Pain Engine
    run_pain_engine "$SCRAPED_FILE" "$skip_ai"
    if [ $? -ne 0 ]; then
        error "Pipeline failed at pain extraction stage"
        return 1
    fi
    echo ""
    
    # Stage 3: Pytch
    run_pytch "$PYTCH_FILE"
    if [ $? -ne 0 ]; then
        error "Pipeline failed at pitch stage"
        return 1
    fi
    echo ""
    
    # Copy DNA pattern to docs if it exists
    if [ -n "$DNA_FILE" ] && [ -f "$DNA_FILE" ]; then
        cp "$DNA_FILE" "$HOME_DIR/modmind_unified/automation/docs/"
        progress "DNA pattern added to evolution library"
    fi
    
    # Summary
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           PIPELINE COMPLETE               ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    echo "  Scraped:  $SCRAPED_FILE"
    echo "  Analyzed: $PYTCH_FILE"
    [ -n "$DNA_FILE" ] && echo "  DNA:      $DNA_FILE"
    echo ""
    echo "  Next: Feed DNA into evolution lab or run Vertical AI assessment"
    echo "        ./MASTER_CONTROL.sh → DNA Evolution Lab"
    
    return 0
}

# ---------------------------------------------------------------------------
# INTERACTIVE MODE
# ---------------------------------------------------------------------------

interactive_menu() {
    banner
    
    while true; do
        echo ""
        echo "What do you want to do?"
        echo "1. Run full pipeline (new query)"
        echo "2. Run on cached data (last scrape)"
        echo "3. Show recent results"
        echo "4. Run Vertical AI on a gap"
        echo "5. Exit"
        echo ""
        
        read -p "Choice: " choice
        
        case "$choice" in
            1)
                echo ""
                read -p "What kind of business / what location? " query
                echo ""
                echo "Use AI analysis (Ollama) or keyword-only?"
                echo "1. AI (slower, better)"
                echo "2. Keyword only (fast, no model needed)"
                read -p "Choice: " ai_choice
                
                skip="false"
                [ "$ai_choice" = "2" ] && skip="true"
                
                run_full_pipeline "$query" "$skip"
                ;;
            2)
                # Find most recent scraped file
                LATEST=$(ls -t "$CACHE_DIR"/*.json 2>/dev/null | head -1)
                if [ -z "$LATEST" ]; then
                    error "No cached scrapes found. Run option 1 first."
                else
                    progress "Using: $LATEST"
                    run_pain_engine "$LATEST" "false"
                    [ $? -eq 0 ] && run_pytch "$PYTCH_FILE"
                fi
                ;;
            3)
                echo ""
                echo "=== Recent Scrapes ==="
                ls -lt "$CACHE_DIR"/*.json 2>/dev/null | head -5
                echo ""
                echo "=== Recent Pain Point Analyses ==="
                ls -lt "$PAIN_DIR"/pytch_*.json 2>/dev/null | head -5
                echo ""
                echo "=== DNA Patterns in Library ==="
                ls "$HOME_DIR/modmind_unified/automation/docs/"*.json 2>/dev/null | head -5
                ;;
            4)
                echo ""
                echo "=== Available Gaps ==="
                # Show gaps from most recent analysis
                LATEST_PYTCH=$(ls -t "$PAIN_DIR"/pytch_*.json 2>/dev/null | head -1)
                if [ -n "$LATEST_PYTCH" ]; then
                    python3 -c "
import json
with open('$LATEST_PYTCH') as f:
    data = json.load(f)
gaps = data.get('patterns', {}).get('gaps', [])
for i, g in enumerate(gaps, 1):
    print(f'{i}. {g.get(\"opportunity\", \"\")} [{g.get(\"market_size_estimate\", \"\")}]')
    print(f'   Solves: {g.get(\"solves_pain_point\", \"\")}')
    print(f'   Type: {g.get(\"automation_type\", \"\")}')
    print()
"
                    echo "Run Vertical AI assessment on which gap? (number or q to quit)"
                    read -p "Gap: " gap_num
                    
                    if [ "$gap_num" != "q" ]; then
                        # Extract gap and feed to vertical-ai
                        python3 -c "
import json, subprocess
with open('$LATEST_PYTCH') as f:
    data = json.load(f)
gaps = data.get('patterns', {}).get('gaps', [])
idx = int('$gap_num') - 1
if 0 <= idx < len(gaps):
    gap = gaps[idx]
    print(f'Assessing opportunity: {gap[\"opportunity\"]}')
    print(json.dumps(gap, indent=2))
"
                    fi
                else
                    error "No analyses yet. Run the pipeline first."
                fi
                ;;
            5)
                echo "Bye."
                exit 0
                ;;
            *)
                echo "Invalid choice"
                ;;
        esac
    done
}

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

# Make sure output dirs exist
mkdir -p "$CACHE_DIR"
mkdir -p "$PAIN_DIR"

# Parse args
if [ $# -eq 0 ]; then
    # No args = interactive
    interactive_menu
elif [ "$1" = "--cached" ]; then
    # Run on last cached scrape
    LATEST=$(ls -t "$CACHE_DIR"/*.json 2>/dev/null | head -1)
    if [ -z "$LATEST" ]; then
        error "No cached scrapes. Run with a query first."
        exit 1
    fi
    banner
    progress "Using cached: $LATEST"
    run_pain_engine "$LATEST" "false"
    [ $? -eq 0 ] && run_pytch "$PYTCH_FILE"
elif [ "$1" = "--skip-ai" ]; then
    # Skip AI, use keyword extraction
    shift
    query="$*"
    run_full_pipeline "$query" "true"
else
    # Direct query
    query="$*"
    run_full_pipeline "$query" "false"
fi
