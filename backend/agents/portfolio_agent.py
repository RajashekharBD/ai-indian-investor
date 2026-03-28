import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

MOCK_RESPONSES = [
    "Based on the current market conditions, I see several opportunities in the Nifty 50 space. Steel stocks like TATASTEEL have shown strong momentum with institutional buying. However, always consider your risk profile before making any decisions.",
    "For your portfolio holdings, I notice you have good exposure to the IT sector through INFY. Given the current rupee movement, IT stocks might see some tailwind. Consider diversifying into banking with HDFCBANK for balance.",
    "Looking at today's FII data, they've been net buyers for the past 5 sessions, which is generally bullish. However, DII selling has been absorbing some of this demand. The Nifty is likely to face resistance at 22,600 levels.",
    "Technical analysis shows RELIANCE is forming a bull flag pattern after its recent rally. RSI at 58 suggests room for more upside. Watch for breakout above 2,900 for momentum confirmation.",
    "For a moderate risk profile like yours, I'd suggest focusing on quality large-caps with strong fundamentals. PSU banks like SBI have been showing relative strength. Always maintain adequate stop losses."
]

class PortfolioAgent:
    def __init__(self):
        self.history = []
        self.response_index = 0
        api_key = os.getenv("GROQ_API_KEY", "")
        
        if api_key and api_key != "your-api-key":
            try:
                import groq
                self.client = groq.Groq(api_key=api_key)
                self.has_groq = True
            except Exception:
                self.has_groq = False
        else:
            self.has_groq = False
        
        self.system_prompt = """You are an expert Indian stock market advisor for retail investors.

Context:
- You have access to real-time market data from NSE India
- You're analyzing stocks for Indian investors
- Focus on Nifty 50 stocks primarily
- Always provide specific numbers, prices, and percentages

Guidelines:
1. Be concise but informative
2. Always cite data sources when possible
3. Explain risks alongside opportunities
4. Tailor advice to the user's risk profile and portfolio
5. Use simple language, avoid jargon

Never give definitive buy/sell recommendations. Always include appropriate disclaimers."""

    async def get_response(
        self,
        message: str,
        portfolio: List[str] = None,
        risk_profile: str = "moderate"
    ) -> dict:
        context = f"User risk profile: {risk_profile}"
        if portfolio:
            context += f"\nUser portfolio holdings: {', '.join(portfolio)}"
        
        try:
            if self.has_groq:
                chat_completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": f"{context}\n\nUser question: {message}"}
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )
                result = chat_completion.choices[0].message.content
            else:
                result = MOCK_RESPONSES[self.response_index % len(MOCK_RESPONSES)]
                self.response_index += 1
            
            self.history.append({
                "user": message,
                "assistant": result,
                "portfolio": portfolio,
                "risk_profile": risk_profile
            })
            
            return {
                "response": result,
                "sources": self._get_relevant_sources(message),
                "confidence": 75,
                "streaming": True
            }
        except Exception as e:
            return {
                "response": f"I'm having trouble processing that request. Please configure your GROQ_API_KEY in the .env file for full functionality.",
                "sources": [],
                "confidence": 0,
                "streaming": False
            }
    
    def _get_relevant_sources(self, query: str) -> List[dict]:
        keywords = query.lower()
        sources = []
        
        if any(word in keywords for word in ["reliance", "infy", "hdfc", "tcs", "itc"]):
            sources.append({
                "title": "NSE India - Corporate Filing",
                "url": "https://www.nseindia.com/companies-listing/corporate-filings-announcements"
            })
        
        if any(word in keywords for word in ["bulk deal", "insider", "fii", "dii"]):
            sources.append({
                "title": "BSE India - Block Deals",
                "url": "https://www.bseindia.com/markets/BlockDeal.html"
            })
        
        return sources[:3]
    
    def get_conversation_history(self) -> List[dict]:
        return self.history[-10:]
