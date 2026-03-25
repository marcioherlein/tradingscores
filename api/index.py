from fastapi import FastAPI

app = FastAPI(title="TradingScores API")


@app.get("/")
def root():
    return {
        "name": "TradingScores",
        "status": "ok",
        "mode": "decision-support",
        "message": "API deployed successfully. UI not added yet. Next step is to expose screener data and build the frontend."
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
