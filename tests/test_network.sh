#!/bin/bash

# Configuration
MAX_RETRIES=10
RETRY_INTERVAL=2

# Helper for exiting with custom codes
fail() {
    echo -e "\n\033[0;31mERROR: $1\033[0m"
    exit $2
}

# Generic wait function
# Usage: wait_for_url <url> <service_name> <error_code>
wait_for_url() {
    local url=$1
    local name=$2
    local code=$3
    
    echo -n "Waiting for $name..."
    for ((i=1; i<=MAX_RETRIES; i++)); do
        if curl -s --fail "$url" > /dev/null; then
            echo -e " [OK]"
            return 0
        fi
        echo -n "."
        sleep $RETRY_INTERVAL
    done
    fail "$name failed to become healthy after $((MAX_RETRIES * RETRY_INTERVAL))s" $code
}

echo "--- Phase 1: Infrastructure Health ---"
wait_for_url "http://localhost:8001/health" "Bot 1" 10
wait_for_url "http://localhost:8002/health" "Bot 2" 10

echo "--- Phase 2: Host Connectivity (Ollama) ---"
# Note: We don't necessarily need to loop here because if the container is up, 
# the network interface should be ready.
podman exec bot1 curl -s -I http://host.containers.internal:11434 | grep "200 OK" > /dev/null \
    || fail "Bot 1 cannot reach Ollama on host" 20

echo "--- Phase 3: Inter-Agent Relay ---"
# Check if Bot 1 can resolve and ping Bot 2 on the internal network
podman exec bot1 curl -s --fail http://bot2:8000/health > /dev/null \
    || fail "Relay path Bot 1 -> Bot 2 is broken (Internal Network)" 30

echo -e "\n\033[0;32m--- ALL TESTS PASSED ---\033[0m"
exit 0