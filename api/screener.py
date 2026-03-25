from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

UNIVERSE = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
    "META", "TSLA", "AVGO", "AMD", "NFLX"
]


@app.get("/")
def screener():
    results = []

    for ticker in UNIVERSE:
        try:
            data = yf.download(ticker, period="1y", progress=False)
            if data.empty:
                continue

            price = data["Close"].iloc[-1]
            ema200 = data["Close"].ewm(span=200).mean().iloc[-1]
            trend_status = "above_ema200" if price > ema200 else "below_ema200"

            results.append({
                "ticker": ticker,
                "price": float(price),
                "ema200": float(ema200),
                "trend_status": trend_status
            })
        except Exception:
            continue

    return results
