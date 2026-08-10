#!/data/data/com.termux/files/usr/bin/bash
# MIND READER: Behavioral Profiling
# "We know what you're thinking before you do."

set -e

TARGET_PID=$1
DURATION=${2:-30} # Seconds
LOOM_DB="$HOME/loom_nat_db.json"

if [[ -z "$TARGET_PID" ]]; then
    echo "Usage: $0 <PID> [DURATION]"
    exit 1
fi

log_event() {
    local event_type="$1"
    local details="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    echo "{"event_id": "$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)", "timestamp": "$timestamp", "agent_role": "Mind Reader", "action": "$event_type", "details": "$details", "target_pid": "$TARGET_PID"}" >> "${LOOM_DB}.log"
}

echo "👁️  Initializing Mind Reader on PID $TARGET_PID..."
log_event "START" "Mind Reader attached"

# Check for strace
if command -v strace >/dev/null; then
    echo "  -> Using strace for deep introspection."
    # Use strace to monitor syscalls briefly
    strace -p "$TARGET_PID" -e trace=file,process,network -o "/tmp/mind_read_$TARGET_PID.log" &
    STRACE_PID=$!
    
    # Monitor log size
    for i in $(seq 1 "$DURATION"); do
        if kill -0 "$TARGET_PID" 2>/dev/null; then
             sleep 1
             # Log anomalies (e.g., failed open calls)
             if grep -q "ENOENT" "/tmp/mind_read_$TARGET_PID.log"; then
                 LAST_ERR=$(grep "ENOENT" "/tmp/mind_read_$TARGET_PID.log" | tail -n 1)
                 log_event "ANOMALY" "File not found: $LAST_ERR"
             fi
        else
             echo "Target died."
             break
        fi
    done
    
    kill "$STRACE_PID" 2>/dev/null || true
    rm "/tmp/mind_read_$TARGET_PID.log" 2>/dev/null || true
else
    echo "  -> Using ps/proc for surface scan (strace not found)."
    # Monitor /proc
    for i in $(seq 1 "$DURATION"); do
        if kill -0 "$TARGET_PID" 2>/dev/null; then
            STATE=$(cat "/proc/$TARGET_PID/stat" 2>/dev/null | cut -d ' ' -f 3)
            THREADS=$(cat "/proc/$TARGET_PID/status" 2>/dev/null | grep Threads | awk '{print $2}')
            echo "  -> State: $STATE | Threads: $THREADS"
            log_event "STATUS" "State: $STATE, Threads: $THREADS"
            sleep 1
        else
            echo "Target died."
            break
        fi
    done
fi

echo "👁️  Mind Read complete."
log_event "STOP" "Mind Reader detached"
