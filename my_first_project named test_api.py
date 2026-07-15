import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("COMPANIES_HOUSE_API_KEY")

company_number = "00000006"

url = f"https://api.company-information.service.gov.uk/company/{company_number}"

response = requests.get(url, auth=(api_key, ""))

print("Status code:", response.status_code)
print(response.json())