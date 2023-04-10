from abc import ABC, abstractmethod
import json
import requests
from bs4 import BeautifulSoup


class WebRequester(ABC):
    @abstractmethod
    def get(self, url):
        pass


class HTMLParser(ABC):
    @abstractmethod
    def parse(self, content):
        pass


class DataTransformer(ABC):
    @abstractmethod
    def transform(self, data):
        pass


class DataWriter(ABC):
    @abstractmethod
    def write(self, data, filename):
        pass


class FundScraper:
    def __init__(self, requester: WebRequester, parser: HTMLParser, transformer: DataTransformer, writer: DataWriter):
        self.requester = requester
        self.parser = parser
        self.transformer = transformer
        self.writer = writer

    def run(self, url, indexes, class_name, filename='data.json'):
        response = self.requester.get(url)
        if response.status_code != 200:
            raise ValueError(f"Error retrieving {url}: {response.status_code}")
        soup = self.parser.parse(response.content)
        data = self.transformer.transform(
            soup.find_all('div', class_=class_name), indexes)
        self.writer.write(data, filename)


class RequestsWebRequester(WebRequester):
    def get(self, url):
        return requests.get(url)


class BeautifulSoupHTMLParser(HTMLParser):
    def parse(self, content):
        return BeautifulSoup(content, "html.parser")


class FundValueTransformer(DataTransformer):
    def transform(self, values, indexes):
        return {"values": [str(values[i].contents[0]).strip().replace('$US', '').replace(',', '')
                           for i in indexes]}


class JSONDataWriter(DataWriter):
    def write(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


scraper = FundScraper(RequestsWebRequester(), BeautifulSoupHTMLParser(
), FundValueTransformer(), JSONDataWriter())

scraper.run(url='https://sprott.com/investment-strategies/physical-commodity-funds/uranium/',
            indexes=[4, 6],
            class_name='fundHeader_value',
            filename='data.json')
