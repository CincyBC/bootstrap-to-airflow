from bs4 import BeautifulSoup
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from plugins.operators.fund_scraper_operator import FundScraperOperator


# Default args used when create a new dag
args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "schedule_interval": "@daily",
}

with DAG(
    dag_id="Functional_Sprott_Scraper",
    schedule_interval="5 20 * * 1-6",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    default_args=args,
    render_template_as_native_obj=True,
    tags=["price", "scraper"],
) as dag:
    scrape_task = FundScraperOperator(
        url="https://sprott.com/investment-strategies/physical-commodity-funds/uranium/"
    )
