import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COMPANIES_HOUSE_API_KEY")

search_terms = ["technology", "finance", "retail", "consulting", "manufacturing"]

all_companies = []

for term in search_terms:
    url = "https://api.company-information.service.gov.uk/search/companies"
    params = {"q": term, "items_per_page": 20}
    response = requests.get(url, auth=(api_key, ""), params=params)

    if response.status_code == 200:
        data = response.json()
        for item in data.get("items", []):
            all_companies.append({
                "company_number": item.get("company_number"),
                "company_name": item.get("title"),
                "company_status": item.get("company_status"),
                "search_term": term,
            })
    else:
        print(f"Failed for '{term}': status {response.status_code}")

    time.sleep(0.3)

df = pd.DataFrame(all_companies)
df = df.drop_duplicates(subset="company_number")
df.to_csv("../data/companies_data.csv", index=False)
print(f"Total unique companies pulled: {len(df)}")
print(df.head(10))