import os
import requests
from dotenv import load_dotenv
# from cachetools import cached, TTLCache

load_dotenv()

API_KEY = os.getenv("TA_API_KEY")
url = "https://api.taapi.io/bulk"

# cache = TTLCache(maxsize=500, ttl=120)

def formatar_analise(dados):
    return """
🟠 Bitcoin:

💰 Preço Atual $USD: {:.2f}
📊 Volume $USD: {:.2f}
📈 RSI: {:.2f}
📉 MACD: {:.2f}
🟢 MACD Sinal: {:.2f}
📏 Média Móvel (10): {:.2f}
📏 Média Móvel (50): {:.2f}
📊 ATR: {:.2f}
⚡️ ADX: {:.2f}
    """.format(
            dados['PRICE'],
            dados['VOLUME'],
            dados['RSI'],
            dados['MACD'],
            dados['MACD Sinal'],
            dados['Média Móvel (sma_10)'],
            dados['Média Móvel (sma_50)'],
            dados['ATR'],
            dados['ADX']
        )

#@cached(cache)
def get_data():
    payload = {
        "secret": API_KEY,
        "construct": {
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "5m",
            "indicators": [
                {"indicator": "price"},
                {"indicator": "volume"},
                {"indicator": "rsi", "period": 14},
                {"indicator": "macd"},
                {"indicator": "sma", "period": 10, "id": "sma_10"},
                {"indicator": "sma", "period": 50, "id": "sma_50"},
                {"indicator": "atr", "period": 14},
                {"indicator": "adx", "period": 14}
            ]
        }
    }

    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    response = resp.json()

    resultado = {}
    for item in response.get("data", []):
        ind = item["indicator"]
        res = item.get("result", {})
        if ind == "macd":
            resultado["MACD"] = res.get("valueMACD")
            resultado["MACD Sinal"] = res.get("valueMACDSignal")
        elif ind.startswith("sma"):
            resultado[f"Média Móvel ({item.get('id')})"] = res.get("value")
        else:
            resultado[ind.upper()] = res.get("value")

    return formatar_analise(resultado) if resultado else "Erro ao obter dados de análise técnica."
