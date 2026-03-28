import pandas as pd
from ta import momentum, trend, volatility

class TechnicalAnalysis:
    @staticmethod
    def calculate_rsi(prices: pd.Series, window: int = 14) -> float:
        rsi = momentum.RSIIndicator(close=prices, window=window)
        return float(rsi.rsi().iloc[-1])
    
    @staticmethod
    def calculate_macd(prices: pd.Series):
        macd = momentum.MACD(close=prices)
        return {
            "macd": float(macd.macd().iloc[-1]),
            "signal": float(macd.macd_signal().iloc[-1]),
            "histogram": float(macd.macd_diff().iloc[-1])
        }
    
    @staticmethod
    def calculate_sma(prices: pd.Series, periods: list = [20, 50, 200]) -> dict:
        result = {}
        for period in periods:
            if len(prices) >= period:
                sma = trend.SMAIndicator(close=prices, window=period)
                result[f"sma_{period}"] = float(sma.sma_indicator().iloc[-1])
        return result
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, window: int = 20) -> dict:
        bb = volatility.BollingerBands(close=prices, window=window)
        return {
            "upper": float(bb.bollinger_hband().iloc[-1]),
            "middle": float(bb.bollinger_mavg().iloc[-1]),
            "lower": float(bb.bollinger_lband().iloc[-1])
        }
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> float:
        atr = volatility.AverageTrueRange(high=high, low=low, close=close, window=window)
        return float(atr.average_true_range().iloc[-1])
    
    @staticmethod
    def detect_support_resistance(prices: pd.Series, window: int = 20) -> dict:
        highs = prices.rolling(window=window).max()
        lows = prices.rolling(window=window).min()
        
        return {
            "resistance": float(highs.iloc[-1]),
            "support": float(lows.iloc[-1]),
            "range": float(highs.iloc[-1] - lows.iloc[-1])
        }
    
    @staticmethod
    def calculate_all(prices: pd.Series, high: pd.Series = None, low: pd.Series = None) -> dict:
        result = {
            "rsi": TechnicalAnalysis.calculate_rsi(prices),
            "macd": TechnicalAnalysis.calculate_macd(prices),
            "sma": TechnicalAnalysis.calculate_sma(prices),
            "bollinger": TechnicalAnalysis.calculate_bollinger_bands(prices),
            "support_resistance": TechnicalAnalysis.detect_support_resistance(prices)
        }
        
        if high is not None and low is not None:
            result["atr"] = TechnicalAnalysis.calculate_atr(high, low, prices)
        
        return result
