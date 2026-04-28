from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional
import uuid, datetime
from server.agent_card import AGENT_CARD
from server.handlers import handle_task

app = FastAPI(title="Echo A2A Agent")

@app.get("/.well-known/agent.json")
async def get_agent_card():
    return AGENT_CARD

@app.get('/health')
async def health():
    return {"status": "ok", "agent": AGENT_CARD["id"]}

class TextPart(BaseModel):
    type: str = 'text'
    text: str

class FilePart(BaseModel):
    type: str = "file"
    url: str
    mimeType: str

class Message(BaseModel):
    role: str
    parts: list[TextPart | FilePart]

class TaskRequest(BaseModel):
    id: str
    sessionId: Optional[str] = None
    message: Message
    metadata: Optional[dict[str, Any]] = None

@app.post('/tasks/send')
async def send_task(request: TaskRequest):
    if not request.message.parts:
        raise HTTPException(status_code=400, detail="message.parts cannot be empty")

    result_text = await handle_task(request)

    return {
        "id": request.id,
        "status": {"state": "completed"},
        "artifacts": [
            {
                "parts": [{"type": "text", "text": result_text}]
            }
        ],
    }
