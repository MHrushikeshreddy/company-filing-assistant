import pandas as pd

filings_df = pd.read_csv("../data/filings_data.csv", dtype={"company_number": str})
filings_df["date"] = pd.to_datetime(filings_df["date"])

filings_df = filings_df.sort_values(["company_number", "date"])

filings_df["days_since_last_filing"] = (
    filings_df.groupby("company_number")["date"].diff().dt.days
)

summary = filings_df.groupby("company_number").agg(
    total_filings=("category", "count"),
    first_filing=("date", "min"),
    last_filing=("date", "max"),
    avg_days_between_filings=("days_since_last_filing", "mean"),
    max_gap_days=("days_since_last_filing", "max"),
).reset_index()

summary.to_csv("../data/filing_summary.csv", index=False)
print(summary)