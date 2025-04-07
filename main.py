import requests
from bs4 import BeautifulSoup

url = 'https://auto.ria.com/uk/legkovie/?page=1'

response = requests.get(url)


soup = BeautifulSoup(response.text, 'lxml')

# extract car brand
brand = soup.find('span', class_='blue bold').text

# extract reneration
generation = soup.find('div', class_='generation').text

# extract price
price = soup.find('span', class_='bold size22 green').text.replace(' ', '')

# extract mileage
mileage = soup.find('li', class_='item-char js-race').text

# extract location
location = soup.find('li', class_='item-char view-location js-location').text


li_el = soup.find('ul', class_='unstyle characteristic').find_all(
    'li', class_='item-char')

fuel_type = li_el[2].text


print(brand)
print('===========================')
print(generation)
print('===========================')
print(price)
print('===========================')
print(mileage)
print('===========================')
print(location)
print('===========================')
print(fuel_type)
