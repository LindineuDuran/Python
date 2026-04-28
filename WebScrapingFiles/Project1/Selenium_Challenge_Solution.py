#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#imports

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

#options = webdriver.ChromeOptions()
#options.add_argument('--incognito')


driver = webdriver.Chrome()
driver.get('http://sdsclub.com')

#links
# Substitua time.sleep(5) por WebDriverWait(driver, 10)

button_one = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu-item-456"]/a')))
button_one.click()

button_two = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="category-career"]//img')))
button_two.click()

try:
    button_close = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".close-icon"))
    )
    button_close.click()
except:
    print("Popup não apareceu")


#add parser
page_source = driver.page_source
soup =  BeautifulSoup(page_source, 'lxml')

#add scrape info
scrape_one = [i.text for i in soup.findAll('span', {'class': 'desc'})]
scrape_two = [i.text for i in soup.findAll('div', {'class': 'single-path-article-content'})]
scrape_three = [i.text for i in soup.findAll('p', {'class': 'name'})]

#assign DF's
df = pd.DataFrame(scrape_one)
df_two = pd.DataFrame(scrape_two)
df_three = pd.DataFrame(scrape_three)

#print data
print(df, df_two, df_three)

time.sleep(10)

driver.quit()

df_scrape_one_clean = df.replace('\n', ' ', )
df_scrape_two_clean = df_two.replace('\n', ' ', )
df_scrape_three_clean = df_three.replace('\n', ' ',)
clean_stack = pd.concat([df_scrape_one_clean, df_scrape_two_clean, df_scrape_three_clean], axis=1)


#https://clasroom.github.com/a/WYb3hT_P


