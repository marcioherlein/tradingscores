import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

UNIVERSE_PATH = "data/universe.csv"
OUTPUT_PATH = "data/latest_factors.csv"


def load_universe():
    df = pd.read_csv(UNIVERSE_PATH)
    return df['ticker'].tolist()


def compute_indicators(df):
    df['ema200'] = df['Close'].ewm(span=200).mean()
    df['sma50'] = df['Close'].rolling(window=50).mean()

    df['return_90d'] = df['Close'].pct_change(90)

    # ATR approximation
    df['high_low'] = df['High'] - df['Low']
    df['atr'] = df['high_low'].rolling(14).mean()
    df['atr_pct'] = df['atr'] / df['Close'] * 100

    return df


def process_ticker(ticker):
    try:
        data = yf.download(ticker, period="1y", progress=False)
        if data.empty:
            return None

        data = compute_indicators(data)
        latest = data.iloc[-1]

        return {
            "ticker": ticker,
            "price": latest['Close'],
            "ema200": latest['ema200'],
            "sma50": latest['sma50'],
            "return_90d": latest['return_90d'],
            "atr_pct": latest['atr_pct']
        }
    except Exception as e:
        print(f"Error {ticker}: {e}")
        return None


def main():
    tickers = load_universe()
    results = []

    for t in tickers:
        print(f"Processing {t}...")
        res = process_ticker(t)
        if res:
            results.append(res)

    df = pd.DataFrame(results)

    # Relative strength ranking
    df['rs_percentile'] = df['return_90d'].rank(pct=True) * 100

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
