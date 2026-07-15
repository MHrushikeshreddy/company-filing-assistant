import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COMPANIES_HOUSE_API_KEY")

company_numbers = [
    "00000006",   # Marine and General Mutual Life Assurance Society (dissolved)
    "00000019",   # Another old-registry company
    "01046209",   # BP p.l.c.
    "00102498",   # Tesco PLC
    "03977902",   # Google UK Limited
    "00445790",   # Marks and Spencer PLC
    "00048839",   # HSBC Holdings PLC
]

results = []

for number in company_numbers:
    url = f"https://api.company-information.service.gov.uk/company/{number}"
    response = requests.get(url, auth=(api_key, ""))

    if response.status_code == 200:
        data = response.json()
        results.append({
            "company_number": data.get("company_number"),
            "company_name": data.get("company_name"),
            "company_status": data.get("company_status"),
            "date_of_creation": data.get("date_of_creation"),
            "type": data.get("type"),
            "jurisdiction": data.get("jurisdiction"),
            "sic_codes": data.get("sic_codes"),
            "registered_office_postal_code": data.get("registered_office_address", {}).get("postal_code"),
        })
    else:
        print(f"Failed for {number}: status {response.status_code}")

    time.sleep(0.3)

df = pd.DataFrame(results)
df.to_csv("companies_data.csv", index=False)
print(df)