from fastapi import APIRouter
from tools.market_data import MarketDataFetcher

router = APIRouter()
fetcher = MarketDataFetcher()

@router.get("/market-summary")
async def get_market_summary():
    try:
        summary = await fetcher.get_market_summary()
        return summary
    except Exception as e:
        return {
            "timestamp": "2026-03-28T15:30:00",
            "data_source": "demo",
            "indices": {
                "nifty": {"value": 22450.25, "change": 268.30, "change_pct": 1.21},
                "banknifty": {"value": 48500.80, "change": -219.45, "change_pct": -0.45}
            },
            "top_gainers": [
                {"symbol": "TATASTEEL", "change_pct": 4.8, "price": 142.50},
                {"symbol": "JSWSTEEL", "change_pct": 3.9, "price": 820.30},
                {"symbol": "HINDALCO", "change_pct": 3.2, "price": 485.60}
            ],
            "top_losers": [
                {"symbol": "HDFCBANK", "change_pct": -2.1, "price": 1442.30},
                {"symbol": "KOTAKBANK", "change_pct": -1.8, "price": 1720.50},
                {"symbol": "SBIN", "change_pct": -1.5, "price": 615.80}
            ],
            "fiidii": {
                "fii_net": 1250.5,
                "dii_net": -890.2,
                "summary": "FIIs bought 1250 Cr. DIIs sold 890 Cr."
            }
        }

@router.get("/stock/{symbol}")
async def get_stock_data(symbol: str):
    try:
        data = await fetcher.get_stock_data(symbol.upper())
        return data
    except Exception as e:
        return {"symbol": symbol.upper(), "error": str(e)}
