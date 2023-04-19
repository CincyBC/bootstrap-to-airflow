FROM python:3.10-slim-buster

WORKDIR /

RUN apt-get update && apt-get upgrade -y
RUN apt-get install gcc nano libpq-dev python3-dev -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /src .

# CMD [ "python3", "scrapers/eviction_scraper.py"]