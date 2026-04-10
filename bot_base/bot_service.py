# @generated
# Reviewed and Edited by the author of the codebase.
#
# This code is part of the Multi-Agent Podman project.
#
# bot_service.py - A simple FastAPI service for a chatbot using Ollama
# This service exposes three endpoints:
# 1. /chat - for chatting with the bot
# 2. /relay/{target_agent} - for relaying messages to another bot
# 3. /health - for health checks
# The bot's name and the model it uses can be configured via environment variables.

from fastapi import FastAPI
from pydantic import BaseModel
import os
import ollama
import httpx

app = FastAPI()

# Environment variables for bot configuration
BOT_NAME = os.getenv("BOT_NAME", "bot-default")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:latest")

# Pydantic model for incoming chat messages
class Message(BaseModel):
    text: str

# Endpoint for chatting with the bot
@app.post("/chat")
async def chat(msg: Message):
    prompt = f"You are {BOT_NAME}. Respond concisely.\nUser: {msg.text}\n{BOT_NAME}:"
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"bot": BOT_NAME, "reply": response["message"]["content"]}

# New endpoint to trigger agent-to-agent talk
@app.post("/relay/{target_agent}")
async def relay(target_agent: str, msg: Message):
    # 1. Bot A thinks of a reply to the user
    my_reply = await chat(msg)
    
    # 2. Bot A sends its reply to Bot B
    # Use the service name from podman-compose as the hostname
    url = f"http://{target_agent}:8000/chat"
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json={"text": my_reply["reply"]})
    
    return {
        "origin_bot": BOT_NAME,
        "my_message": my_reply["reply"],
        "target_bot": target_agent,
        "target_reply": res.json()
    }

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}