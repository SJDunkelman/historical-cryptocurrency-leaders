# Historical Cryptocurrency Leaders

Scrape the historical cryptocurrency market leaders by market cap from 2013 up to present using CoinMarketCap. Data capture includes:

* Name / Ticker
* Market Cap
* Price
* Circulating Supply

This data was captured as part of backtesting an investment strategy, of which the preliminary research can be [found here]. Data such as this is especially invaluable for strategies focused on high-liquidity coins, and can help combat survivorship bias.

## Requirements

CoinMarketCap is protected by Cloud Flare, and will eventually hit you with a CAPTCHA after several pages. To avoid this, the script will detect when you have been asked and will then pause scraping until the user has manually changed their IP and defeated the CAPTCHA. Therefore, to use this script for any meaningfully large date range I recommend you have a VPN installed.

## Installation

1. Clone this repo

```bash
git clone https://github.com/SJDunkelman/historical-cryptocurrency-leaders
```

2. Create virtual environment requirements.txt

```
cd historical-cryptocurrency-leaders
virtualenv venv/
source venv/bin/activate
pip install -r requirements.txt
```

3. Download chromedriver for your version of Chrome then change the filepath in <code>const.py</code>

The original intention for this data was only to scrape the top 30 coins during the 2020s. If you want to extend this to all those listed (maximum 200), then you must alter lines <code>107-110</code> so that the coins are not filtered.

## Usage

```bash
python main.py
```

