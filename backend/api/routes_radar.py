from fastapi import APIRouter, Query
from typing import List, Optional
from agents.radar_agent import RadarAgent

router = APIRouter()
agent = RadarAgent()

@router.get("/radar")
async def get_opportunities(
    date: Optional[str] = Query(None),
    signals: Optional[str] = Query("bulk_deal,insider_trading,volume_spike")
):
    signal_list = signals.split(",") if signals else ["bulk_deal", "insider_trading", "volume_spike"]
    
    try:
        alerts = await agent.scan_opportunities(date=date, signals=signal_list)
        return {
            "date": date or "today",
            "alerts": alerts,
            "top_picks": [a["symbol"] for a in alerts[:3]] if alerts else []
        }
    except Exception as e:
        return {
            "date": date or "today",
            "alerts": [],
            "top_picks": [],
            "error": str(e)
        }

@router.get("/radar/alerts/{alert_id}")
async def get_alert_detail(alert_id: str):
    return agent.get_alert_detail(alert_id)
