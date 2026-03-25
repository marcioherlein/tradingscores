# TradingScores Scoring Model v2

## Objective

This model is built for a discretionary decision-support workflow, not auto-trading.

The question it tries to answer is:

**Which strong NYSE/NASDAQ stocks are currently offering a cleaner pullback entry without obvious technical damage?**

## Design principles

- Favor strong stocks in established uptrends
- Prefer controlled pullbacks over extended momentum spikes
- Penalize names that are too extended or in weak trend structure
- Keep the model transparent and explainable

## Factors

### 1. Trend quality (0-30)
- Price above EMA200
- EMA200 slope positive
- Price above SMA50

### 2. Relative strength (0-25)
- 90-day return percentile versus the selected universe

### 3. Pullback quality (0-25)
- Pullback from 20-day high is present but not too deep
- 5-day return is negative or flat
- Relative volume on the pullback is not excessive

### 4. Volatility control (0-10)
- Lower ATR percent receives a better score

### 5. Market regime (0-10)
- SPY above EMA200 and 20-day trend not broken

## Interpretation

Higher score does **not** mean buy automatically.

It means the stock deserves more attention because it combines:
- acceptable market regime
- healthy trend structure
- relative strength
- potentially favorable entry timing

## Score bands

- 80-100: high-priority review candidate
- 65-79: good watchlist name
- 50-64: mixed / secondary
- below 50: weak fit for this model

## Known limitations

- Uses daily price/volume only
- No earnings-event filter yet
- No sector-relative filter yet
- No liquidity floor yet beyond universe selection
- No backtest evidence yet
