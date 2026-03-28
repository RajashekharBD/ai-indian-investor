from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agents.portfolio_agent import PortfolioAgent

router = APIRouter()
agent = PortfolioAgent()

class ChatRequest(BaseModel):
    message: str
    portfolio: Optional[List[str]] = []
    risk_profile: Optional[str] = "moderate"

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await agent.get_response(
            message=request.message,
            portfolio=request.portfolio,
            risk_profile=request.risk_profile
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history")
async def get_history():
    return {"history": agent.get_conversation_history()}
