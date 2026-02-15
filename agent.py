# pip install selenium beautifulsoup4 pandas tqdm openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

countries = ["Egypt", "Saudi-Arabia", "United-Arab-Emirates"]
pages = 50
all_data = []

print("🔍 Fetching data from FastBase using Selenium...")

for country in countries:
    base_url = f"https://www.fastbase.com/countryindex/{country}/R/Real-estate-agency"
    print(f"\n Fetching: {country}")

    for page in tqdm(range(1, pages + 1), desc=f"{country}"):
        url = f"{base_url}?page={page}"
        driver.get(url)
        time.sleep(7)  

        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select("table.table tbody tr")

        for row in rows:
            name = row.select_one(".td_cinx_cname")
            contact = row.select_one(".td_cinx_con_per")
            email = row.select_one(".td_cinx_email")
            phone = row.select_one(".td_cinx_phone")
            city = row.select_one(".td_cinx_city")
            street = row.select_one(".td_cinx_street")

            def text_of(cell):
                if not cell:
                    return ""
                return cell.get("title", cell.get_text(strip=True))

            all_data.append({
                "Company Name": text_of(name),
                "Contact Person": text_of(contact),
                "Email": text_of(email),
                "Phone": text_of(phone),
                "Street": text_of(street),
                "City": text_of(city),
                "Country": country.replace("-", " ")
            })

driver.quit()

df = pd.DataFrame(all_data)
df.to_excel("agents_multi.xlsx", index=False)

print(f"\n Done! Extracted {len(all_data)} agents and saved to 'fastbase_agents_multi.xlsx'")
