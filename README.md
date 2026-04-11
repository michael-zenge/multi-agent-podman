
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
    
-   **Orchestration**: A sequence that runs the Startup, then the Test script, and finally the Cleanup.## 🧪 Testing Strategy

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
