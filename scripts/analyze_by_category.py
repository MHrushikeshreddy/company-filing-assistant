import pandas as pd

filings_df = pd.read_csv("../data/filings_data.csv", dtype={"company_number": str})
filings_df["date"] = pd.to_datetime(filings_df["date"])

category_summary = filings_df.groupby(["company_number", "category"]).agg(
    count=("date", "count"),
    first_date=("date", "min"),
    last_date=("date", "max"),
).reset_index()

category_summary = category_summary.sort_values(["company_number", "count"], ascending=[True, False])

category_summary.to_csv("../data/category_summary.csv", index=False)
print(category_summary.to_string(index=False))