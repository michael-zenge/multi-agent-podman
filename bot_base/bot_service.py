from fastapi import FastAPI
from pydantic import BaseModel
import os
import ollama

app = FastAPI()

BOT_NAME = os.getenv("BOT_NAME", "bot-default")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:latest")

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(msg: Message):
    prompt = f"You are {BOT_NAME}. Respond concisely.\nUser: {msg.text}\n{BOT_NAME}:"
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"bot": BOT_NAME, "reply": response["message"]["content"]}

@app.get("/health")
def health():
    return {"status": "ok"}
