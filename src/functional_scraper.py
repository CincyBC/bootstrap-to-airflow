import requests
from bs4 import BeautifulSoup
import json


def web_call(url):  # Extract
    r = requests.get(url)
    if r.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")
    return soup


def get_fund_values(soup, index, class_name):  # Transform
    fund_values = soup.find_all('div', class_=class_name)
    value = fund_values[index].contents
    return str(value[0]).strip().replace('$US', '').replace(',', '')


def write_json(data, filename='data.json'):  # Load
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    soup = web_call(
        url='https://sprott.com/investment-strategies/physical-commodity-funds/uranium/')
    data = {}
    data['shareprice'] = get_fund_values(soup, 4, 'fundHeader_value')
    data['u3o8_stock'] = get_fund_values(soup, 6, 'fundHeader_value')
    write_json(data)
