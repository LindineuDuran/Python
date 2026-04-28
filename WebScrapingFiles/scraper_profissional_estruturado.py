#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time


BASE_URL = "http://sdsclub.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

MAX_RETRIES = 3
REQUEST_TIMEOUT = 10


# --------------------------------------------------
# LOG CONFIG
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# --------------------------------------------------
# HTTP REQUEST WITH RETRY
# --------------------------------------------------

def fetch_page(url):

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            logging.info(f"Requesting page: {url}")

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            return response.text

        except requests.exceptions.RequestException as e:

            logging.warning(f"Attempt {attempt} failed: {e}")

            if attempt == MAX_RETRIES:
                logging.error("Max retries reached.")
                raise

            time.sleep(2)


# --------------------------------------------------
# PARSE HTML
# --------------------------------------------------

def parse_html(html):

    soup = BeautifulSoup(html, "lxml")

    descriptions = [i.get_text(strip=True) for i in soup.select("span.desc")]
    contents = [i.get_text(strip=True) for i in soup.select("div.single-path-article-content")]
    names = [i.get_text(strip=True) for i in soup.select("p.name")]

    df1 = pd.DataFrame(descriptions, columns=["description"])
    df2 = pd.DataFrame(contents, columns=["content"])
    df3 = pd.DataFrame(names, columns=["name"])

    df = pd.concat([df1, df2, df3], axis=1)

    return df


# --------------------------------------------------
# PAGINATION DISCOVERY
# --------------------------------------------------

def discover_pages():

    pages = [BASE_URL]

    # exemplo simples de paginação
    # se o site tiver links tipo /page/2 /page/3 etc

    for i in range(2, 6):
        pages.append(f"{BASE_URL}/page/{i}")

    return pages


# --------------------------------------------------
# MAIN SCRAPER
# --------------------------------------------------

def run_scraper():

    logging.info("Starting scraper")

    pages = discover_pages()

    all_data = []

    for url in pages:

        html = fetch_page(url)

        df = parse_html(html)

        all_data.append(df)

        time.sleep(1)

    final_df = pd.concat(all_data, ignore_index=True)

    return final_df


# --------------------------------------------------
# EXPORT DATA
# --------------------------------------------------

def export_data(df):

    logging.info("Exporting data")

    df.to_csv("sdsclub_data.csv", index=False)

    df.to_excel("sdsclub_data.xlsx", index=False)

    logging.info("Export completed")


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

def main():

    df = run_scraper()

    print(df.head())

    export_data(df)

    logging.info("Scraping finished successfully")


if __name__ == "__main__":
    main()