from common import open_selenium_driver
from bs4 import BeautifulSoup as bs4


if __name__=="__main__":
    screener_url = 'https://messari.io/screener/supply-and-marketcap-EB1755C2'

    driver = open_selenium_driver()

    driver.get(screener_url)
    html = driver.page_source.encode('utf-8')
    soup = bs4(html, 'html.parser')

    width = driver.execute_script("return document.body.scrollWidth")
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")

    # driver.quit()
