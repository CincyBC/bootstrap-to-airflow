from abc import ABC, abstractmethod
import json
import requests
from bs4 import BeautifulSoup
from yaml import safe_load


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

    def run(self, url, indexes, value_names, class_name, filename='data.json'):
        response = self.requester.get(url)
        if response.status_code != 200:
            raise ValueError(f"Error retrieving {url}: {response.status_code}")
        soup = self.parser.parse(response.content)
        data = {}
        for index, index_number in enumerate(indexes):
            data = self.transformer.transform(
                soup.find_all('div', class_=class_name), data, index_number, value_names[index])
        self.writer.write(data, filename)


class RequestsWebRequester(WebRequester):
    def get(self, url):
        return requests.get(url)


class BeautifulSoupHTMLParser(HTMLParser):
    def parse(self, content):
        return BeautifulSoup(content, "html.parser")


class FundValueTransformer(DataTransformer):
    def transform(self, values, dictionary: dict, index: int, value_name: str):
        dictionary[value_name] = str(values[index].contents[0]).strip().replace(
            '$US', '').replace(',', '')
        return dictionary


class JSONDataWriter(DataWriter):
    def write(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':
    config = safe_load(open('config.yml', 'r'))

    scraper = FundScraper(RequestsWebRequester(), BeautifulSoupHTMLParser(
    ), FundValueTransformer(), JSONDataWriter())

    for key, value in config.items():
        for class_name in value['class_name']:
            for tag, indexes in class_name.items():
                scraper.run(url=value['url'],
                            class_name=tag,
                            indexes=[i for i in indexes.keys()],
                            value_names=[v for v in indexes.values()],
                            filename=f"{key}.json")
