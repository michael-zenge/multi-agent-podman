# @generated
# Reviewed and Edited by the author of the codebase.
#
# This code is part of the Multi-Agent Podman project.
#
# Dockerfile - Dockerfile for the chatbot service

FROM python:3.12-slim

# Keep curl for testing/health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Copy requirements from the workspace root (where the context starts) 
COPY requirements.txt .

# 2. Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the bot code from the bot_base folder
COPY bot_base/bot_service.py .

# Use the DNS name as the default
ENV OLLAMA_HOST="http://host.containers.internal:11434"

EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "bot_service:app", "--host", "0.0.0.0", "--port", "8000"]