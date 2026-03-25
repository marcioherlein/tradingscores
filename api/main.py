from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="TradingScores API")


@app.get("/")
def root():
    return {"status": "ok", "service": "TradingScores API"}


@app.get("/screener")
def get_screener():
    try:
        df = pd.read_csv("data/scored.csv")
        top = df.sort_values(by="score", ascending=False).head(10)
        return top.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e), "message": "Run data pipeline first to generate scored.csv"}


@app.get("/health")
def health():
    return {"status": "healthy"}
