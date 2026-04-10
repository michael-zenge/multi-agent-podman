#!/bin/bash
# @generated
MAX_RETRIES=5
COUNT=0

echo "Waiting for Bot1 to be healthy..."
# Use 'until' to wait until curl SUCCEEDS (exit code 0)
until curl -s --fail http://127.0.0.1:8001/health > /dev/null; do
    printf '.'
    sleep 2
done
echo -e "\nBot1 is UP!"

echo -e "\nRunning Network Connectivity Tests..."
echo "Testing Bot 1 Health..."
curl -s http://localhost:8001/health | grep "ok" || exit 1

echo "Testing Bot 2 Health..."
curl -s http://localhost:8002/health | grep "ok" || exit 1

echo "Testing Container-to-Host (Ollama) connectivity..."
podman exec bot1 curl -s -I http://host.containers.internal:11434 | grep "200 OK" || exit 1

echo "ALL SYSTEMS GO"