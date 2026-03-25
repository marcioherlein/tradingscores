import pandas as pd

INPUT_PATH = "data/latest_factors.csv"
OUTPUT_PATH = "data/scored.csv"


def compute_score(row):
    score = 0

    if row['price'] > row['ema200']:
        score += 15

    if row['price'] > row['sma50']:
        score += 10

    if row['rs_percentile'] > 90:
        score += 20
    elif row['rs_percentile'] > 80:
        score += 15

    if row['atr_pct'] < 5:
        score += 10

    return score


def main():
    df = pd.read_csv(INPUT_PATH)

    df['score'] = df.apply(compute_score, axis=1)

    df = df.sort_values(by='score', ascending=False)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Top ranked stocks:")
    print(df[['ticker', 'score']].head(10))


if __name__ == "__main__":
    main()
