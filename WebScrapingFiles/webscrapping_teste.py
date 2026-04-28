#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://sdsclub.com"


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_page(html):

    soup = BeautifulSoup(html, "lxml")

    descriptions = [i.get_text(strip=True) for i in soup.select("span.desc")]
    contents = [i.get_text(strip=True) for i in soup.select("div.single-path-article-content")]
    names = [i.get_text(strip=True) for i in soup.select("p.name")]

    df1 = pd.DataFrame(descriptions, columns=["description"])
    df2 = pd.DataFrame(contents, columns=["content"])
    df3 = pd.DataFrame(names, columns=["name"])

    df = pd.concat([df1, df2, df3], axis=1)

    return df


def main():

    print("Baixando página...")

    html = get_page(BASE_URL)

    print("Extraindo dados...")

    df = parse_page(html)

    print(df)

    print("\nSalvando arquivo...")

    df.to_excel("sdsclub_scraping.xlsx", index=False)

    print("Concluído ✔")


if __name__ == "__main__":
    main()