import pandas as pd
import random

random.seed(42)
df = pd.read_csv("filings_data.csv")
df["company_number"] = df["company_number"].astype(str).str.zfill(8)

companies = df["company_number"].unique().tolist()
sample_companies = random.sample(companies, min(15, len(companies)))

rows = []

for company in sample_companies:
    company_df = df[df["company_number"] == company]
    categories = company_df["category"].unique().tolist()

    if "dissolution" in categories or "gazette" in categories:
        rows.append({
            "question": f"Was company {company} dissolved?",
            "expected_answer_contains": "dissolv"
        })
    else:
        rows.append({
            "question": f"Was company {company} dissolved?",
            "expected_answer_contains": "no"
        })

    if "accounts" in categories:
        accounts_desc = company_df[company_df["category"] == "accounts"]["description"].iloc[0]
        if "dormant" in accounts_desc:
            expected = "dormant"
        elif "full" in accounts_desc.lower():
            expected = "full"
        elif "micro" in accounts_desc.lower():
            expected = "micro"
        else:
            expected = accounts_desc.split("-")[-1]
        rows.append({
            "question": f"What type of accounts did company {company} file?",
            "expected_answer_contains": expected
        })

    officer_rows = company_df[company_df["category"] == "officers"]
if not officer_rows.empty:
    has_director_change = officer_rows["description"].str.contains("director", case=False).any()
    if has_director_change:
        rows.append({
            "question": f"Did company {company} have any director changes?",
            "expected_answer_contains": "director"
        })
    else:
        rows.append({
            "question": f"Did company {company} have any secretary changes?",
            "expected_answer_contains": "secretary"
        })

    if "address" in categories:
        rows.append({
            "question": f"Did company {company} have a registered office address change?",
            "expected_answer_contains": "address"
        })

    if "confirmation-statement" in categories:
        rows.append({
            "question": f"Did company {company} file a confirmation statement?",
            "expected_answer_contains": "confirmation"
        })

eval_df = pd.DataFrame(rows)
eval_df.to_csv("eval_questions_large.csv", index=False)
print(f"Generated {len(eval_df)} questions across {len(sample_companies)} companies.")
print(eval_df.head(10).to_string())