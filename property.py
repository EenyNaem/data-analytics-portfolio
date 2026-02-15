from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import re

houses_data = []

driver = webdriver.Chrome()

for i in range(1, 300):
    url = f'https://www.propertyfinder.eg/en/search?l=2254&c=1&fu=0&ob=mr&page={i}'
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    houses = soup.find_all('li', attrs={'data-testid': True})
    if not houses:
        print(f"No houses found on page {i}")
        continue

    for house in houses:
        try:
            # Price
            price_tag = house.find('p', class_=re.compile('price'))
            price = price_tag.text.strip() if price_tag else 'N/A'

            # Location
            location_tag = house.find('p', class_=re.compile('location'))
            location = location_tag.text.strip() if location_tag else 'N/A'

            # Property Type
            property_type_tag = house.find('p', class_=re.compile('property-type'))
            property_type = property_type_tag.text.strip() if property_type_tag else 'N/A'

            # Listed Since
            time_listed_tag = house.find('p', class_=re.compile('publish-info'))
            time_listed = time_listed_tag.text.strip() if time_listed_tag else 'N/A'

            # Bedrooms, Bathrooms, Area
            details_tags = house.find_all('p', class_=re.compile('details-item'))
            bedrooms = details_tags[0].text.strip() if len(details_tags) > 0 else 'N/A'
            bathrooms = details_tags[1].text.strip() if len(details_tags) > 1 else 'N/A'
            area = details_tags[2].text.strip() if len(details_tags) > 2 else 'N/A'

            
            houses_data.append({
                'Price': price,
                'Location': location,
                'Property Type': property_type,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Area': area,
                'Listed Since': time_listed
            })

        except Exception as e:
            print(f"Error on page {i}: {e}")
            continue

driver.quit()

# Save data to CSV
df = pd.DataFrame(houses_data)
df.to_csv('property_fider_data.csv', index=False, encoding='utf-8-sig')

print("Data has been scraped and saved to property_finder_data.csv")
