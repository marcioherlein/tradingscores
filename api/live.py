from fastapi import FastAPI
import pandas as pd
import yfinance as yf

app = FastAPI()

UNIVERSE = [
    "AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA","AVGO","AMD","NFLX",
    "JPM","BAC","GS","V","MA","UNH","LLY","XOM","CVX","HD"
]


def compute_indicators(df):
    df['ema200'] = df['Close'].ewm(span=200).mean()
    df['sma50'] = df['Close'].rolling(50).mean()

    df['return_90d'] = df['Close'].pct_change(90)
    df['return_5d'] = df['Close'].pct_change(5)

    df['high_20'] = df['Close'].rolling(20).max()
    df['distance_from_high'] = (df['Close'] - df['high_20']) / df['high_20']

    df['volume_avg20'] = df['Volume'].rolling(20).mean()
    df['rel_volume'] = df['Volume'] / df['volume_avg20']

    df['atr'] = (df['High'] - df['Low']).rolling(14).mean()
    df['atr_pct'] = df['atr'] / df['Close'] * 100

    return df


def process_ticker(ticker):
    data = yf.download(ticker, period="1y", progress=False)
    if data.empty:
        return None

    data = compute_indicators(data)
    latest = data.iloc[-1]

    return {
        "ticker": ticker,
        "price": float(latest['Close']),
        "ema200": float(latest['ema200']),
        "sma50": float(latest['sma50']),
        "return_90d": float(latest['return_90d']),
        "return_5d": float(latest['return_5d']),
        "distance_from_high": float(latest['distance_from_high']),
        "rel_volume": float(latest['rel_volume']),
        "atr_pct": float(latest['atr_pct'])
    }


def compute_score(row, market_regime):
    score = 0

    if row['price'] > row['ema200']:
        score += 15
    if row['price'] > row['sma50']:
        score += 10

    score += row['rs_percentile'] * 0.25

    if -0.08 < row['distance_from_high'] < -0.02:
        score += 15
    elif -0.15 < row['distance_from_high'] < -0.08:
        score += 10

    if row['return_5d'] < 0:
        score += 5

    if row['rel_volume'] < 1:
        score += 5

    score += max(0, 10 - row['atr_pct'])

    score += market_regime * 10

    return score


@app.get("/live")
def live_screener():
    results = []

    for t in UNIVERSE:
        try:
            res = process_ticker(t)
            if res:
                results.append(res)
        except Exception:
            continue

    df = pd.DataFrame(results)

    if df.empty:
        return {"error": "No data"}

    df['rs_percentile'] = df['return_90d'].rank(pct=True) * 100

    spy = yf.download("SPY", period="1y", progress=False)
    spy['ema200'] = spy['Close'].ewm(span=200).mean()
    market_regime = int(spy.iloc[-1]['Close'] > spy.iloc[-1]['ema200'])

    df['score'] = df.apply(lambda r: compute_score(r, market_regime), axis=1)

    df = df.sort_values(by='score', ascending=False)

    return df.head(10).to_dict(orient="records")
