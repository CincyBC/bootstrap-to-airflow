import requests
from unittest.mock import patch
from bs4 import BeautifulSoup
import json
import pytest
from functional_scraper import web_call, get_fund_values, write_json


@pytest.fixture
def mock_requests_get():
    with patch.object(requests, 'get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_requests_failed_get():
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value.status_code = 400
        yield mock_get


def test_web_call(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.content = '<html><head></head><body><div></div></body></html>'
    result = web_call('http://www.example.com')
    assert isinstance(result, BeautifulSoup)


def test_failed_web_call(mock_requests_failed_get):
    result = web_call('http://www.example.com')
    assert result == 400


def test_get_fund_values():
    soup = BeautifulSoup(
        '<html><head></head><body><div class="fund">$US1,000.00</div></body></html>', 'html.parser')
    result = get_fund_values(soup, 0, 'fund')
    assert result == '1000.00'


def test_write_json(tmp_path):
    data = {'foo': 'bar'}
    filename = tmp_path / 'test.json'
    write_json(data, filename)
    with open(filename) as f:
        result = json.load(f)
    assert result == data
