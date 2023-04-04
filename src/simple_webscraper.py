import requests
from bs4 import BeautifulSoup

url = 'https://sprott.com/investment-strategies/physical-commodity-funds/uranium/'
r = requests.get(url)
if r.status_code == 200:
    soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")

fund_values = soup.find_all('div', class_='fundHeader_value')
shareprice = fund_values[4].contents
shareprice_value = str(shareprice[0]).strip().replace('$US', '')

u3o8 = fund_values[6].contents
u3o8_stock = str(u3o8[0]).strip().replace(',', '')
