# @generated

#import pytest
import respx
from httpx import Response
from unittest.mock import patch
from fastapi.testclient import TestClient
from bot_base.bot_service import app

client = TestClient(app)

# 1. Test the health endpoint
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# 2. Test the chat endpoint
@patch('ollama.chat')
def test_chat_logic(mock_ollama):
    mock_ollama.return_value = {
        "message": {"content": "Test reply from AI"}
    }
    
    response = client.post("/chat", json={"text": "Hello"})
    assert response.status_code == 200
    assert "reply" in response.json()
    assert response.json()["bot"] == "bot-default"

# 3. Test the relay endpoint
@respx.mock  # This intercepts the outgoing HTTP call to the other bot
@patch('ollama.chat')
def test_relay_logic(mock_ollama, respx_mock):
    # Mock Bot 1's local Ollama response
    mock_ollama.return_value = {
        "message": {"content": "I am sending this to the other bot."}
    }

    # Mock the outgoing network call to 'bot2'
    # This simulates Bot 2's API response
    target_url = "http://bot2:8000/chat"
    respx_mock.post(target_url).mock(return_value=Response(
        200, 
        json={"bot": "bot2", "reply": "Acknowledged by Bot 2"}
    ))

    payload = {"text": "Forward this message"}
    response = client.post("/relay/bot2", json=payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["origin_bot"] == "bot-default"
    assert data["target_bot"] == "bot2"
    assert data["target_reply"]["reply"] == "Acknowledged by Bot 2"