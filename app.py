from fastapi import FastAPI
import yfinance as yf

app = FastAPI(title="TradingScores")

UNIVERSE = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
    "META", "TSLA", "AVGO", "AMD", "NFLX"
]


@app.get("/")
def root():
    return {
        "name": "TradingScores",
        "status": "ok",
        "message": "Deployment fixed. Use /screener for live data."
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/screener")
def screener():
    results = []

    for ticker in UNIVERSE:
        try:
            data = yf.download(ticker, period="1y", progress=False)
            if data.empty:
                continue

            price = float(data["Close"].iloc[-1])
            ema200 = float(data["Close"].ewm(span=200).mean().iloc[-1])

            results.append({
                "ticker": ticker,
                "price": price,
                "ema200": ema200,
                "trend_status": "above_ema200" if price > ema200 else "below_ema200"
            })
        except Exception:
            continue

    return results
