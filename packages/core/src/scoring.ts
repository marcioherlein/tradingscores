export type StockData = {
  price: number
  ema200: number
  sma50: number
  rsPercentile: number
  relVolume: number
  distanceTo52wLow: number
  atrPercent: number
}

export function computeWarrenScore(data: StockData): number {
  let score = 0

  // Trend
  if (data.price > data.ema200) score += 15
  if (data.price > data.sma50) score += 10

  // Momentum
  if (data.rsPercentile > 90) score += 20
  else if (data.rsPercentile > 80) score += 15

  // Pullback
  if (data.distanceTo52wLow < 0.25) score += 10

  // Volume
  if (data.relVolume < 0.8) score += 10

  // Volatility
  if (data.atrPercent < 5) score += 10

  return score
}
