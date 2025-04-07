import requests
from bs4 import BeautifulSoup
import re
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

for count in range(1, 10):
    sleep(0.7)
    url = f"https://auto.ria.com/uk/search/?lang_id=4&page={count}&countpage=100&category_id=1&custom=1&abroad=2"

    response = requests.get(url, headers=headers)
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
        price = price_tag.text.replace(' ', '').strip() if price_tag else None

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
        data_update = date_span.get('data-update-date') if date_span else None

        # Print all data
        print(f"ID: {ad_id}")
        print(f"Link: {link}")
        print(f"Name: {car_name}")
        print(f"Year: {year}")
        print(f"Generation: {generation_info}")
        print(f"Price: {price}")
        print(f"Mileage: {mileage}")
        print(f"Location: {location}")
        print(f"Fuel/Engine: {fuel_type}")
        print(f"Transmission: {transmission}")
        print(f"State number: {state_number}")
        print(f"VIN: {vin_code}")
        print(f"Date added: {data_add}")
        print(f"Date updated: {data_update}")
        print('=' * 40)
