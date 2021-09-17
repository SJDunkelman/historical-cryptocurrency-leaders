import requests as req
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs4
from datetime import datetime
from common import open_selenium_driver
from tqdm import tqdm
import re

# Scraping top 30 projects by market cap using coinmarketcap
# start_date = datetime(2021, 1, 1)
# end_date = datetime(2021, 9, 17)
# backtest_date_range = pd.date_range(start=start_date, end=end_date)
# backtest_timestamp_range = [d.strftime("%Y%m%d") for d in backtest_date_range]

# Get all dates of historical snapshots listed
snapshot_index_url = 'https://coinmarketcap.com/historical/'
resp = req.get(snapshot_index_url)
soup = bs4(resp.text, 'html.parser')
links = soup.find_all('a', {'class': 'historical-link'})
links = [l['href'] for l in links]

driver = open_selenium_driver()
actions = ActionChains(driver)

target_url = 'https://coinmarketcap.com/'
bottom_button_xpath = '//*[@id="__next"]/div[1]/div[2]/div/div[1]/div[3]/div[2]/div[2]/a[1]'
historical_market_data = {}


def scrape_coins(coinmarket_soup, already_scraped):
    table = coinmarket_soup.find('tbody')
    for row in table.find_all('tr', {'class': 'cmc-table-row'}):
        row_data = []
        for div in row.find_all('div'):
            row_data.append(div.text)
        if len(row_data):
            already_scraped.append({'rank': row_data[0],
                                  'full_name': row_data[1],
                                  'ticker': row_data[2],
                                  'market_cap': row_data[3],
                                  'price': row_data[4],
                                  'circulating_supply': row_data[5]})
    return already_scraped


for resource in tqdm(links):
# resource = links[10]
    coin_market_url = f'https://coinmarketcap.com/{resource}'
    date = re.search(r'\d+', resource).group()
    date = datetime.strptime(date, "%Y%m%d").date()
    driver.get(coin_market_url)

    # Check for cloudflare
    try:
        button = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/button')
    except:
        i = input('Have you countered cloudflare with new IP? (y/n)')
        if i.lower() == 'y':
            driver.get(coin_market_url)

    html = driver.page_source.encode("utf-8")
    soup = bs4(html, 'lxml')

    snapshot_data = scrape_coins(soup, [])
    print(snapshot_data)

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element = driver.find_element_by_xpath(bottom_button_xpath)
    # actions.move_to_element(element).perform()
    # snapshot_data = scrape_coins(soup, snapshot_data)

    historical_market_data[date] = snapshot_data
    time.sleep(10)

driver.quit()
