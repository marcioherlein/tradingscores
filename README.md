# TradingScores

A decision-support tool for screening stocks, assigning a transparent 0-100 Warren Score, ranking a defined universe, and surfacing the top ideas for manual trading.

## Product direction

This is **not** an auto-trading system.

The goal is to help a human trader decide what deserves attention by:

1. loading a stock universe
2. computing factor-based scores for each name
3. ranking the universe
4. surfacing the top candidates
5. tracking a model top-10 watchlist/portfolio

## Core principles

- No black box scoring
- Every factor must be explainable
- Every score must be reproducible
- Strategy ideas must be testable before risking capital
- Manual decision-making remains in control

## Core loop

1. Load stock universe
2. Compute factors for each stock
3. Normalize or bucket factor values
4. Compute Warren Score (0-100)
5. Rank all stocks
6. Display top candidates
7. Track paper performance and score drift

## Initial repo scope

- Product docs
- Transparent scoring engine scaffold
- TypeScript monorepo structure
- Placeholder web app shell

## Current status

- [x] Product vision
- [x] Initial scoring model draft
- [x] Core scoring engine scaffold
- [ ] Market data pipeline
- [ ] Screener UI
- [ ] Portfolio view
- [ ] Historical testing
- [ ] Alerting

## Repository structure

```text
.
├── apps
│   └── web
├── docs
│   ├── product-spec.md
│   └── scoring-model.md
├── packages
│   └── core
└── package.json
```

## Warning

A screener is easy to build. A robust edge is not.

Do not treat a high score as a trading signal by itself. The score is only a decision-support input and must be used alongside market regime, risk management, liquidity, and execution discipline.
