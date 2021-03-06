from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import os
import const
import requests
import pandas as pd
from typing import Union
import re

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'


def open_selenium_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = const.CHROME_BINARY_PATH
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(const.CHROME_DRIVER_PATH, options=options)


def get_soup_from_request(url: str):
    resp = requests.get(url)
    soup = bs4(resp.content, 'html.parser')
    return soup


def record_failed_scrape(scraped_object_name: str, reason: str, output_file: str):
    with open(output_file, 'a+') as file:
        file.write(f'{scraped_object_name} failed when scraping {reason}')
        file.write('\n')


def clear_failed_log(output_file: str):
    if os.path.isfile(output_file):
        os.remove(output_file)


def append_csv(existing_file: str, dataframe: pd.DataFrame, index: bool = False):
    if not os.path.isfile(existing_file):
        dataframe.to_csv(existing_file, index=index)
    else:
        existing = pd.read_csv(existing_file, index_col=index)
        existing = existing.append(dataframe)
        existing.to_csv(existing_file, index=index)


def preprocess_numeric(number: Union[int, float, str]) -> float:
    if type(number) == str:
        number = number.replace(',', '')
        number = re.sub(r'\s+', '', number)
        numeric = float(re.search(r'[\d.]+', number).group())
        if re.search(r'(?i)m', number) is not None:
            numeric = numeric * 1E6
        elif re.search(r'(?i)k', number) is not None:
            numeric = numeric * 1E3
        return numeric
    return number
