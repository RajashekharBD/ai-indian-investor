from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from agents.analysis_agent import AnalysisAgent

router = APIRouter()
agent = AnalysisAgent()

class AnalyzeRequest(BaseModel):
    symbol: str
    timeframe: str = "1D"
    lookback_days: int = 90

@router.post("/analyze")
async def analyze_stock(request: AnalyzeRequest):
    try:
        result = await agent.analyze(
            symbol=request.symbol.upper(),
            timeframe=request.timeframe,
            lookback_days=request.lookback_days
        )
        return result
    except Exception as e:
        return {
            "symbol": request.symbol.upper(),
            "error": str(e),
            "patterns_detected": [],
            "recommendation": "ERROR"
        }

@router.get("/analyze/{symbol}")
async def quick_analyze(
    symbol: str,
    timeframe: str = Query("1D"),
    lookback_days: int = Query(90)
):
    return await analyze_stock(AnalyzeRequest(
        symbol=symbol,
        timeframe=timeframe,
        lookback_days=lookback_days
    ))
