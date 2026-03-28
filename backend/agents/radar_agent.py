import random
from typing import List, Optional, Dict
from datetime import datetime

class RadarAgent:
    def __init__(self):
        self.alerts_cache = {}
        self._generate_mock_alerts()
    
    def _generate_mock_alerts(self):
        base_alerts = [
            {
                "id": "alert_001",
                "type": "bulk_deal",
                "symbol": "TATASTEEL",
                "action": "BUY",
                "volume_multiplier": 5.2,
                "price_change": 4.8,
                "description": "5x average volume with 4.8% price increase",
                "signal_strength": "STRONG",
                "insight": "Institutional buying detected. Usually precedes 8-12% upside in 30 days.",
                "price": 142.50,
                "target": 155,
                "stop_loss": 135,
                "source": "demo"
            },
            {
                "id": "alert_002",
                "type": "insider_trading",
                "symbol": "HDFCBANK",
                "action": "BUY",
                "insider_name": "Promoter Group",
                "shares": 50000,
                "value_crores": 12.5,
                "insight": "Promoter buying at current levels indicates high conviction.",
                "price": 1442.30,
                "target": 1520,
                "stop_loss": 1380,
                "source": "demo"
            },
            {
                "id": "alert_003",
                "type": "volume_spike",
                "symbol": "RELIANCE",
                "action": "WATCH",
                "volume_multiplier": 3.8,
                "price_change": 2.1,
                "description": "3.8x average volume with moderate price rise",
                "signal_strength": "MODERATE",
                "insight": "Accumulation phase likely. Watch for breakout above 2,900.",
                "price": 2847.50,
                "target": 2950,
                "stop_loss": 2780,
                "source": "demo"
            },
            {
                "id": "alert_004",
                "type": "bulk_deal",
                "symbol": "JSWSTEEL",
                "action": "BUY",
                "volume_multiplier": 4.5,
                "price_change": 3.9,
                "description": "4.5x volume surge with steel sector rally",
                "signal_strength": "STRONG",
                "insight": "Steel sector momentum. Target 12% upside in near term.",
                "price": 820.30,
                "target": 890,
                "stop_loss": 790,
                "source": "demo"
            },
            {
                "id": "alert_005",
                "type": "insider_trading",
                "symbol": "INFY",
                "action": "BUY",
                "insider_name": "CFO Purchase",
                "shares": 25000,
                "value_crores": 8.2,
                "insight": "CFO buying shares in open market. Usually bullish signal.",
                "price": 1456.20,
                "target": 1520,
                "stop_loss": 1420,
                "source": "demo"
            },
            {
                "id": "alert_006",
                "type": "volume_spike",
                "symbol": "HINDALCO",
                "action": "BUY",
                "volume_multiplier": 4.1,
                "price_change": 3.2,
                "description": "Aluminum prices up globally, stock following",
                "signal_strength": "MODERATE",
                "insight": "Commodity tailwind. Target 510 in 2-3 weeks.",
                "price": 485.60,
                "target": 510,
                "stop_loss": 470,
                "source": "demo"
            },
            {
                "id": "alert_007",
                "type": "breakout",
                "symbol": "SBIN",
                "action": "BUY",
                "breakout_level": 620,
                "price_change": 2.8,
                "description": "Breaking above 6-month resistance at 620",
                "signal_strength": "STRONG",
                "insight": " PSU bank rally continuing. Target 650-680.",
                "price": 625.50,
                "target": 680,
                "stop_loss": 600,
                "source": "demo"
            },
            {
                "id": "alert_008",
                "type": "bulk_deal",
                "symbol": "ADANIPORTS",
                "action": "WATCH",
                "volume_multiplier": 6.2,
                "price_change": -1.5,
                "description": "Unusual volume with price decline - possible distribution",
                "signal_strength": "CAUTION",
                "insight": "Monitor for further weakness. Support at 780.",
                "price": 820.30,
                "target": 850,
                "stop_loss": 780,
                "source": "demo"
            }
        ]
        
        for alert in base_alerts:
            self.alerts_cache[alert["id"]] = alert
    
    async def scan_opportunities(
        self,
        date: Optional[str] = None,
        signals: Optional[List[str]] = None
    ) -> List[dict]:
        filtered_alerts = []
        signals = signals or ["bulk_deal", "insider_trading", "volume_spike"]
        
        for alert in self.alerts_cache.values():
            if alert["type"] in signals:
                filtered_alerts.append(alert)
        
        random.shuffle(filtered_alerts)
        return filtered_alerts[:6]
    
    def get_alert_detail(self, alert_id: str) -> dict:
        return self.alerts_cache.get(alert_id, {"error": "Alert not found"})
    
    def get_top_picks(self, count: int = 3) -> List[str]:
        strong_signals = [
            a for a in self.alerts_cache.values()
            if a.get("signal_strength") == "STRONG"
        ]
        return [a["symbol"] for a in strong_signals[:count]]
