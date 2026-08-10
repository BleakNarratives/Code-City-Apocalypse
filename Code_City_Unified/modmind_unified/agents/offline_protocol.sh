#!/data/data/com.termux/files/usr/bin/bash
# 🛡️ OFFLINE AGENT PROTOCOL
# Enables agents to work with cached data when offline

# Global Configuration
OFFLINE_DIR="$HOME/modmind_unified/offline_cache"
LOG_FILE="$HOME/modmind_unified/logs/offline_operations.log"
INTERCOM="$HOME/modmind_unified/intercom.sh"

# Create offline cache directory
mkdir -p "$OFFLINE_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

echo "=== 🛡️ OFFLINE AGENT PROTOCOL ACTIVATED ==="
echo "Status: $(if ping -c 1 8.8.8.8 &>/dev/null; then echo "ONLINE"; else echo "OFFLINE"; fi)"
echo ""

# Check connectivity
check_connection() {
    if ping -c 1 8.8.8.8 &>/dev/null; then
        echo "ONLINE"
        return 0
    else
        echo "OFFLINE"
        return 1
    fi
}

# Cache data for offline use
cache_data() {
    local data_type="$1"
    local data_content="$2"
    local cache_file="$OFFLINE_DIR/${data_type}_cache.json"
    
    echo "${"data_type": "$data_type", "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)", "content": $data_content}" > "$cache_file"
    echo "✅ Cached: $data_type"
}

# Retrieve cached data
get_cached_data() {
    local data_type="$1"
    local cache_file="$OFFLINE_DIR/${data_type}_cache.json"
    
    if [ -f "$cache_file" ]; then
        cat "$cache_file"
        return 0
    else
        echo "❌ No cached data for: $data_type"
        return 1
    fi
}

# Offline intercom logging
offline_intercom() {
    local type="$1"
    local session="$2"
    local agent="$3"
    local role="$4"
    local topic="$5"
    local message="$6"
    
    # Try online intercom first
    if [ -x "$INTERCOM" ] && check_connection; then
        "$INTERCOM" "$type" "$session" "$agent" "$role" "$topic" "$message"
    else
        # Offline logging
        local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        echo "{\"ts\":\"$timestamp\",\"session\":\"$session\",\"agent\":\"$agent\",\"role\":\"$role\",\"source\":\"offline\",\"type\":\"$type\",\"topic\":\"$topic\",\"text\":\"$message\",\"offline_cache\":true}" >> "$LOG_FILE"
        echo "[OFFLINE LOG] $type | $agent | $topic"
    fi
}

# Synchronize offline logs when back online
sync_offline_logs() {
    if [ -f "$LOG_FILE" ] && check_connection; then
        echo "🔄 Synchronizing offline logs..."
        while IFS= read -r line; do
            if [[ $line == *"offline_cache":true* ]]; then
                # Extract and re-send to main intercom
                session=$(echo "$line" | grep -o '"session":"[^"]*"' | cut -d'"' -f4)
                agent=$(echo "$line" | grep -o '"agent":"[^"]*"' | cut -d'"' -f4)
                role=$(echo "$line" | grep -o '"role":"[^"]*"' | cut -d'"' -f4)
                type=$(echo "$line" | grep -o '"type":"[^"]*"' | cut -d'"' -f4)
                topic=$(echo "$line" | grep -o '"topic":"[^"]*"' | cut -d'"' -f4)
                text=$(echo "$line" | grep -o '"text":"[^"]*"' | cut -d'"' -f4)
                
                "$INTERCOM" "$type" "$session" "$agent" "$role" "$topic" "$text"
            fi
        done < "$LOG_FILE"
        
        # Clear offline logs after sync
        > "$LOG_FILE"
        echo "✅ Offline logs synchronized"
    fi
}

# Main offline agent handler
handle_offline_operation() {
    local agent_name="$1"
    local operation="$2"
    local data="$3"
    
    offline_intercom "TASK" "offline" "$agent_name" "worker" "offline_operation" "Starting: $operation"
    
    # Try to get cached data
    if get_cached_data "$operation"; then
        offline_intercom "INFO" "offline" "$agent_name" "worker" "cache_hit" "Using cached data for $operation"
        # Process cached data
        echo "Processing: $operation with cached data"
        sleep 2
        offline_intercom "RESULT" "offline" "$agent_name" "worker" "operation_complete" "Successfully completed $operation offline"
    else
        offline_intercom "WARN" "offline" "$agent_name" "worker" "cache_miss" "No cached data for $operation - attempting fallback"
        
        # Fallback to basic operation
        case "$operation" in
            "system_check")
                echo "Offline system check:"
                echo "- CPU: $(cat /proc/cpuinfo | grep "processor" | wc -l) cores"
                echo "- Memory: $(free -h | grep "Mem:" | awk '{print $2}')"
                echo "- Storage: $(df -h / | grep "^/" | awk '{print $4}') free"
                ;;
            "agent_status")
                echo "Offline agent status:"
                echo "- Self-Healing: $(ls agents/*.sh 2>/dev/null | wc -l) agents available"
                echo "- Task Agents: $(ls swarm/tasks/*.txt 2>/dev/null | wc -l) tasks queued"
                ;;
            "dna_analysis")
                echo "Offline DNA analysis:"
                echo "- Patterns: $(ls automation/docs/*.md 2>/dev/null | wc -l) available"
                echo "- Last modified: $(ls -t automation/docs/*.md 2>/dev/null | head -1 | xargs stat -c %y 2>/dev/null || echo "N/A")"
                ;;
            *)
                echo "Unknown offline operation: $operation"
                ;;
        esac
        
        offline_intercom "RESULT" "offline" "$agent_name" "worker" "fallback_complete" "Completed $operation with fallback method"
    fi
}

# Test offline capabilities
test_offline_mode() {
    echo "Testing offline agent capabilities..."
    
    # Test 1: System check offline
    handle_offline_operation "test_agent" "system_check" ""
    
    # Test 2: Agent status offline  
    handle_offline_operation "test_agent" "agent_status" ""
    
    # Test 3: DNA analysis offline
    handle_offline_operation "test_agent" "dna_analysis" ""
    
    echo "✅ Offline testing complete"
}

# Main menu
while true; do
    echo "OFFLINE PROTOCOL MENU:"
    echo "1. 📡 Test Offline Operations"
    echo "2. 💾 Cache Current Data"
    echo "3. 🔄 Sync Offline Logs"
    echo "4. 📊 View Offline Cache"
    echo "5. ❌ Exit"
    echo ""
    
    read -p "Select option: " choice
    
    case "$choice" in
        1) test_offline_mode ;;
        2) 
            echo "Caching current system data..."
            cache_data "system_metrics" "$(cat /proc/cpuinfo | grep "processor" | wc -l)"
            cache_data "agent_count" "$(ls agents/*.sh 2>/dev/null | wc -l)"
            cache_data "task_queue" "$(ls swarm/tasks/*.txt 2>/dev/null | wc -l)"
            ;;
        3) sync_offline_logs ;;
        4) echo "Offline Cache Contents:"; ls -la "$OFFLINE_DIR/" ;;
        5) exit 0 ;;
        *) echo "Invalid option!" ;;
    esac
done