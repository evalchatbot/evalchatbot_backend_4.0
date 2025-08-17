from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
from backend.agents.chatbot_agent import ChatbotAgent
from backend.api.auth import get_current_user, AuthUser

router = APIRouter(prefix="/chatbot", tags=["chatbot"])
agent = ChatbotAgent()

class ChatbotAskRequest(BaseModel):
    session_id: str
    question: str
    genre: str

class ChatbotAskResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    context: List[Dict[str, Any]]
    metadata: Dict[str, Any]

@router.post("/ask", response_model=ChatbotAskResponse)
async def ask_chatbot(req: ChatbotAskRequest, current: AuthUser = Depends(get_current_user)) -> ChatbotAskResponse:
    try:
        result = await agent.ask(
            user_id=current.user_id,
            session_id=req.session_id,
            question=req.question,
            genre=req.genre
        )
        return ChatbotAskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
