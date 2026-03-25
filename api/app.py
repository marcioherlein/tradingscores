from fastapi import FastAPI
import pandas as pd
import yfinance as yf

app = FastAPI()

UNIVERSE = [
    "AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA","AVGO","AMD","NFLX"
]

@app.get("/")
def root():
    return {"message": "Use /live"}

@app.get("/live")
def live():
    results = []

    for t in UNIVERSE:
        try:
            data = yf.download(t, period="1y", progress=False)
            if data.empty:
                continue

            price = data["Close"].iloc[-1]
            ema200 = data["Close"].ewm(span=200).mean().iloc[-1]

            score = 1 if price > ema200 else 0

            results.append({
                "ticker": t,
                "price": float(price),
                "score": score
            })

        except:
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)
