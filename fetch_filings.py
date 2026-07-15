import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COMPANIES_HOUSE_API_KEY")

df = pd.read_csv("companies_data.csv", dtype={"company_number": str})
company_numbers = df["company_number"].tolist()

print("Company numbers loaded:", company_numbers)

filing_rows = []

for number in company_numbers:
    url = f"https://api.company-information.service.gov.uk/company/{number}/filing-history"
    response = requests.get(url, auth=(api_key, ""))

    print(f"{number} -> status {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        print(f"  items found: {len(items)}")
        for item in items:
            filing_rows.append({
                "company_number": number,
                "category": item.get("category"),
                "description": item.get("description"),
                "date": item.get("date"),
                "type": item.get("type"),
            })

    time.sleep(0.3)

filings_df = pd.DataFrame(filing_rows)
filings_df.to_csv("filings_data.csv", index=False)
print(filings_df.head(20))
print("Total filings pulled:", len(filings_df))