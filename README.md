
# Multi-Agent Podman System

This project implements a modular, multi-agent AI system using **FastAPI** and **Ollama**, orchestrated within **Podman** containers. The architecture supports agent-to-agent relaying and host-side GPU acceleration.

## 🚀 Key Achievements

*  **Containerized AI Agents**: Fully containerized FastAPI services designed to interact with a host-managed Ollama instance.

*  **Network Relay Architecture**: Integrated routing allowing agents to communicate internally while accessing the host's GPU resources via `host.containers.internal`.

*  **Dual-Layer Testing**: A robust testing strategy covering both internal Python logic (unit) and container networking (integration).

*  **Automated Lifecycle**: VS Code Task integration for "one-click" environment startup, testing, and cleanup.

## 🛠️ Workspace Setup

### 1. Python Environment

Create an isolated sandbox to ensure dependency stability:
```bash
python3 -m venv venv-chatbots
source venv-chatbots/bin/activate
pip install -r requirements.txt
```

### 2. VS Code Configuration

Since `.vscode/tasks.json` is excluded from version control via `.gitignore`, you must manually create it in the `.vscode/` folder to enable the automated testing suite. This file should define:

-   **Startup**: `podman-compose -p agent-test -f ./compose/podman-compose.yml up -d`
    
-   **Cleanup**: `podman-compose -p agent-test -f ./compose/podman-compose.yml down`
    
-   **Orchestration**: A sequence that runs the Startup, then the Test script, and finally the Cleanup.

## 🕹️ Using the Bots (Manual Testing)

Once your containers are running, you can talk to them directly from your computer's terminal using a tool called `curl`. This mimics how a website or a mobile app would "speak" to the bots.

### 1. Direct Chat (Talking to Bot 1)

Use this command to send a message directly to **Bot 1**. It will process your text and respond back in the terminal.

```bash
curl -X POST http://localhost:8001/chat \
     -H "Content-Type: application/json" \
     -d '{"text": "Who are you?"}'
```

### 2. Inter-Agent Relay (Bot 1 talking to Bot 2)

This is the "Multi-Agent" magic. This command sends a message to **Bot 1**, but tells it to forward that message to **Bot 2** over the internal container network. Bot 2 will then process it and send the answer back through Bot 1.

```bash
curl -X POST http://localhost:8001/relay/bot2 \
     -H "Content-Type: application/json" \
     -d '{"text": "Tell the other bot that Linux is awesome."}'
```

### 💡 Quick Explanation for Beginners:

-   **`curl`**: A command-line tool used to transfer data to a server.
    
-   **`-X POST`**: Tells the bot you are "posting" (sending) new information to it.
    
-   **`http://localhost:8001`**: The "address" of your bot on your computer.
    
-   **`-H ...`**: A "Header." It tells the bot, "Hey, I'm sending this in a format called JSON."
    
-   **`-d '{"text": "..."}'`**: The actual "Data" or message you want the bot to read.

## 🧪 Testing Strategy

The project uses a "Fail-Fast" testing hierarchy:

### Endpoint Unit Tests (`/tests/test_endpoints.py`)

-   **Goal**: Verifies internal Python logic and API route mapping.
    
-   **Tech**: `pytest`, `TestClient`, and `respx` for mocking inter-agent HTTP calls.
    
-   **Benefit**: Runs without starting containers or using VRAM.

### Network Integration Tests (`/tests/test_network.sh`)

-   **Goal**: Verifies the "physical" infrastructure and container connectivity.
    
-   **Diagnostic Exit Codes**:
    
    -   **10**: Infrastructure Failure (Containers didn't start/health check failed).
        
    -   **20**: Host Connectivity Failure (Cannot reach Ollama on the host).
        
    -   **30**: Relay Failure (Bot 1 cannot communicate with Bot 2).

## 📋 Automation Workflow

The project is configured to use a **VS Code Build Task** (`Ctrl+Shift+B`):

1.  **Startup**: Spins up the container group `agent-test` using the compose file in `./compose/`.
    
2.  **Execution**: Runs `test_network.sh` from the `./tests/` directory with a retry-loop to wait for service readiness.
    
3.  **Cleanup**: Executes `podman-compose down` immediately after tests finish (regardless of pass/fail) to free up system memory and GPU resources.

----------

**Note on Development**: The codebase and automation scripts were generated in collaboration with **Gemini 3 Flash** and have been fully reviewed and verified by the author.
