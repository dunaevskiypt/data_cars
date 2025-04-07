import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep


car_data = []

for count in range(1, 2):
    sleep(0.7)
    url = f"https://auto.ria.com/uk/search/?lang_id=4&page={count}&countpage=100&category_id=1&custom=1&abroad=2"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Find all car cards on the page
        car_cards = soup.find_all('section', class_='ticket-item')

        for card in car_cards:
            # Link and ID
            ad_link = card.find('a', class_='address')
            link = ad_link.get('href') if ad_link else None

            ad_id = None
            if link:
                match = re.search(r'_(\d+)\.html', link)
                ad_id = match.group(1) if match else None

            # Car name and year
            car_name = ad_link.find('span').text.strip(
            ) if ad_link and ad_link.find('span') else None
            year = ad_link.text.strip().replace(car_name, '').strip() if car_name else None

            # Generation / version / power
            gen_block = card.find('div', class_='generation')
            generation_info = gen_block.text.strip() if gen_block else None

            # Price
            price_tag = card.find('span', class_='bold size22 green')
            price = price_tag.text.replace(
                ' ', '').strip() if price_tag else None

            # Mileage
            mileage_tag = card.find('li', class_='item-char js-race')
            mileage = mileage_tag.text.strip() if mileage_tag else None

            # Location
            location_tag = card.find(
                'li', class_='item-char view-location js-location')
            location = location_tag.text.strip() if location_tag else None

            # Fuel type and transmission
            li_items = card.find('ul', class_='unstyle characteristic')
            li_elements = li_items.find_all(
                'li', class_='item-char') if li_items else []

            fuel_type = li_elements[2].text.strip() if len(
                li_elements) > 2 else None
            transmission = li_elements[3].text.strip() if len(
                li_elements) > 3 else None

            # State number and VIN
            base_info = card.find('div', class_='base_information')

            state_number = None
            vin_code = None
            if base_info:
                state_span = base_info.find('span', class_='state-num')
                if state_span:
                    state_number = state_span.contents[0].strip()

                vin_span = base_info.find('span', class_='label-vin')
                if vin_span:
                    vin_inner = vin_span.find_all('span')
                    vin_code = vin_inner[0].text.strip() if vin_inner else None

            # Dates
            footer = card.find('div', class_='footer_ticket')
            date_span = footer.find('span', attrs={
                                    'data-add-date': True, 'data-update-date': True}) if footer else None
            data_add = date_span.get('data-add-date') if date_span else None
            data_update = date_span.get(
                'data-update-date') if date_span else None

            # status check
            sale_status = "sale"
            sold_date = None
            if footer:
                sold_span = footer.find('span', attrs={'data-sold-date': True})
                if sold_span:
                    sale_status = "sold"
                    sold_date = sold_span.get('data-sold-date')

            # add data in dictionary
            car_info = {
                "id": ad_id,
                "link": link,
                "brand": car_name,
                "year": year,
                "generation": generation_info,
                "price": price,
                "mileage": mileage,
                "location": location,
                "fuel_engine": fuel_type,
                "transmission": transmission,
                "state_number": state_number,
                "vin": vin_code,
                "date_added": data_add,
                "date_updated": data_update,
                "sale_status": sale_status,
                "sold_date": sold_date
            }

            # add data in list
            car_data.append(car_info)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")

# save data in json
with open('car_data.json', 'w', encoding='utf-8') as f:
    json.dump(car_data, f, ensure_ascii=False, indent=4)

print("Data has been saved to car_data.json.")
