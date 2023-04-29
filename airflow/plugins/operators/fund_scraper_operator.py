import requests
from bs4 import BeautifulSoup
import json
from airflow.models.baseoperator import BaseOperator


class FundScraperOperator(BaseOperator):
    def __init__(self, url):
        self.url = url

    def web_call(self):  # Extract
        r = requests.get(self.url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            return soup
        else:
            return r.status_code

    def get_fund_values(self, soup, index, class_name, replace_list):  # Transform
        fund_values = soup.find_all('div', class_=class_name)
        value = fund_values[index].contents
        for x in replace_list:
            value = value.replace(x, '')
        return str(value[0]).strip()

    def write_json(self, data, filename='data.json'):  # Load
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def execute(self):
        soup = self.web_call()
        data = {}
        data['shareprice'] = self.get_fund_values(
            soup, 4, 'fundHeader_value', ['$US', ','])
        data['u3o8_stock'] = self.get_fund_values(
            soup, 6, 'fundHeader_value', ['$US', ','])
        self.write_json(data)
