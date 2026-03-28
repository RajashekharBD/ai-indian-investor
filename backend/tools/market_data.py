import yfinance as yf
from typing import Dict, List, Optional
import random
from datetime import datetime

class MarketDataFetcher:
    def __init__(self):
        self.base_nse_url = "https://www.nseindia.com/"
        self.session = None
    
    async def get_market_summary(self) -> Dict:
        try:
            nifty = yf.Ticker("^NSEI")
            banknifty = yf.Ticker("^NSEBANK")
            
            nifty_data = nifty.history(period="1d")
            banknifty_data = banknifty.history(period="1d")
            
            nifty_price = nifty_data['Close'].iloc[-1] if not nifty_data.empty else None
            nifty_prev = nifty_data['Open'].iloc[0] if not nifty_data.empty else None
            banknifty_price = banknifty_data['Close'].iloc[-1] if not banknifty_data.empty else None
            banknifty_prev = banknifty_data['Open'].iloc[0] if not banknifty_data.empty else None
            
            if nifty_price and nifty_prev:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "data_source": "yfinance",
                    "indices": {
                        "nifty": {
                            "value": round(nifty_price, 2),
                            "change": round(nifty_price - nifty_prev, 2),
                            "change_pct": round((nifty_price - nifty_prev) / nifty_prev * 100, 2) if nifty_prev else 0
                        },
                        "banknifty": {
                            "value": round(banknifty_price, 2),
                            "change": round(banknifty_price - banknifty_prev, 2),
                            "change_pct": round((banknifty_price - banknifty_prev) / banknifty_prev * 100, 2) if banknifty_prev else 0
                        }
                    },
                    "top_gainers": self._get_top_movers("gainers"),
                    "top_losers": self._get_top_movers("losers"),
                    "fiidii": self._get_fiidii_data()
                }
        except Exception as e:
            print(f"yfinance error: {e}")
        
        return self._get_mock_summary()
    
    def _get_top_movers(self, direction: str) -> List[Dict]:
        gainers = [
            {"symbol": "TATASTEEL", "change_pct": 4.8, "price": 142.50},
            {"symbol": "JSWSTEEL", "change_pct": 3.9, "price": 820.30},
            {"symbol": "HINDALCO", "change_pct": 3.2, "price": 485.60}
        ]
        losers = [
            {"symbol": "HDFCBANK", "change_pct": -2.1, "price": 1442.30},
            {"symbol": "KOTAKBANK", "change_pct": -1.8, "price": 1720.50},
            {"symbol": "SBIN", "change_pct": -1.5, "price": 615.80}
        ]
        return gainers if direction == "gainers" else losers
    
    def _get_fiidii_data(self) -> Dict:
        return {
            "fii_net": 1250.5,
            "dii_net": -890.2,
            "summary": "FIIs bought 1250 Cr. DIIs sold 890 Cr."
        }
    
    async def get_stock_data(self, symbol: str) -> Dict:
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            data = ticker.history(period="1d")
            
            if not data.empty:
                close = data['Close'].iloc[-1]
                open_price = data['Open'].iloc[0]
                high = data['High'].iloc[-1]
                low = data['Low'].iloc[-1]
                volume = int(data['Volume'].iloc[-1])
                
                return {
                    "symbol": symbol,
                    "price": round(close, 2),
                    "open": round(open_price, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "volume": volume,
                    "change": round(close - open_price, 2),
                    "change_pct": round((close - open_price) / open_price * 100, 2),
                    "source": "yfinance"
                }
        except Exception as e:
            print(f"Stock data error for {symbol}: {e}")
        
        return self._get_mock_stock(symbol)
    
    def _get_mock_summary(self) -> Dict:
        return {
            "timestamp": datetime.now().isoformat(),
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
    
    def _get_mock_stock(self, symbol: str) -> Dict:
        price = random.uniform(500, 3000)
        change = random.uniform(-50, 50)
        return {
            "symbol": symbol,
            "price": round(price, 2),
            "open": round(price - change/2, 2),
            "high": round(price + abs(change) * 0.5, 2),
            "low": round(price - abs(change) * 0.5, 2),
            "volume": random.randint(1000000, 10000000),
            "change": round(change, 2),
            "change_pct": round(change / price * 100, 2),
            "source": "demo"
        }
