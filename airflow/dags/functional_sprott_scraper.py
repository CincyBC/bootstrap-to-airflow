from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task


# Default args used when create a new dag
args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 2, 27),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@daily',
}

with DAG(
    dag_id='Functional_Sprott_Scraper',
    schedule_interval='5 20 * * 1-6',
    default_args=args,
    render_template_as_native_obj=True,
    tags=['price', 'scraper']
) as dag:

    def web_call(url):  # Extract
        import requests
        r = requests.get(url)
        if r.status_code == 200:
            soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")
            return soup
        else:
            return r.status_code

    def get_fund_values(soup, index, class_name):  # Transform
        fund_values = soup.find_all('div', class_=class_name)
        value = fund_values[index].contents
        return str(value[0]).strip().replace('$US', '').replace(',', '')

    def write_json(data, filename='data.json'):  # Load
        import json
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @task()
    def execute_scraper():
        soup = web_call(
            url='https://sprott.com/investment-strategies/physical-commodity-funds/uranium/')
        data = {}
        data['shareprice'] = get_fund_values(soup, 4, 'fundHeader_value')
        data['u3o8_stock'] = get_fund_values(soup, 6, 'fundHeader_value')
        write_json(data)

    execute_scraper()
