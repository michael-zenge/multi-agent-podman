FROM python:3.12-slim

# Work directory inside the container
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn ollama

# Copy your bot code
COPY bot_service.py .

# Default environment variables (can be overridden at runtime)
ENV BOT_NAME="bot-default"
ENV MODEL_NAME="llama3.2:latest"

# IMPORTANT for rootless Podman:
# 10.0.2.2 is the host gateway inside slirp4netns
ENV OLLAMA_HOST="http://10.0.2.2:11434"

# Expose the bot's internal port
EXPOSE 8000

# Start the FastAPI service
CMD ["uvicorn", "bot_service:app", "--host", "0.0.0.0", "--port", "8000"]
