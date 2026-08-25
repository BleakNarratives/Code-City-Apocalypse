#!/usr/bin/env bash
# start_crash_arena.sh — Launch code city crash-to-monster pipeline
set -euo pipefail

CODE_CITY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_PORT="${CITY_API_PORT:-8765}"
FEEDER_POLL="${CRASH_FEED_POLL:-5}"
SCAN_PATH="${CITY_SCAN_PATH:-${CODE_CITY_DIR}}"

echo "═══ CODE CITY CRASH ARENA ═══"
echo "City dir: ${CODE_CITY_DIR}"
echo "Scan path: ${SCAN_PATH}"
echo "API port: ${API_PORT}"
echo "Feeder poll: ${FEEDER_POLL}s"
echo ""

# 1️⃣ Start the City API server
echo "[1/3] Starting Code City API..."
CITY_SCAN_PATH="$SCAN_PATH" python3 "$CODE_CITY_DIR/code_city_api.py" &
API_PID=$!
sleep 2

if kill -0 "$API_PID" 2>/dev/null; then
    echo "  ✓ API running (pid $API_PID) on http://127.0.0.1:${API_PORT}"
else
    echo "  ✗ API failed to start"
    exit 1
fi

# 2️⃣ Start the crash feeder daemon
echo "[2/3] Starting crash feeder..."
python3 "$CODE_CITY_DIR/crash_feeder.py" \
    --url "http://127.0.0.1:${API_PORT}/crash" \
    --poll "$FEEDER_POLL" &
FEEDER_PID=$!

if kill -0 "$FEEDER_PID" 2>/dev/null; then
    echo "  ✓ Feeder running (pid $FEEDER_PID) — polling every ${FEEDER_POLL}s"
else
    echo "  ✗ Feeder failed to start"
    kill "$API_PID" 2>/dev/null
    exit 1
fi

echo "[3/3] Arena is live!"
echo ""
echo "════════════════════════════════════════════"
echo "  CRASH ARENA ACTIVE"
echo "  API: http://127.0.0.1:${API_PORT}/city"
echo "  Health: http://127.0.0.1:${API_PORT}/health"
echo "  Spawns: http://127.0.0.1:${API_PORT}/spawns"
echo "  Feeder PID: ${FEEDER_PID}"
echo "  API PID: ${API_PID}"
echo ""
echo "  Press Ctrl+C to stop"
echo "════════════════════════════════════════════"
echo ""

# Cleanup on exit
cleanup() {
    echo ""
    echo "═══ SHUTTING DOWN ARENA ═══"
    kill "$FEEDER_PID" 2>/dev/null || true
    kill "$API_PID" 2>/dev/null || true
    wait "$FEEDER_PID" 2>/dev/null || true
    wait "$API_PID" 2>/dev/null || true
    echo "  All processes stopped"
    echo "═══ ARENA CLOSED ═══"
}
trap cleanup EXIT

# Tail the city state every 10 seconds
while true; do
    sleep 10
    echo ""
    echo "─── City State $(date +%H:%M:%S) ───"
    curl -s "http://127.0.0.1:${API_PORT}/city" 2>/dev/null | \
        python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f'  Buildings: {d.get(\"buildings\",\"?\")} | Spawns: {d[\"spawn_count\"]} | Disasters: {d.get(\"disasters\",\"?\")} | Monsters: {d.get(\"monsters\",\"?\")}')
    for s in d.get('recent_spawns', [])[-3:]:
        print(f'    {s.get(\"monster_symbol\",\"?\")} {s.get(\"monster_type\",\"?\")} [{s.get(\"error_type\",\"?\")}]')
except: pass
" 2>/dev/null || echo "  (API unreachable)"
done