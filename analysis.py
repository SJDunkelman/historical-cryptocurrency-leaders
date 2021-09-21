import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

data_sources = {'BTC': 'data/historical_data_bitcoin_20210917191220.csv',
                'XRP': 'data/historical_data_xrp_20210917191122.csv',
                'LTC': 'data/historical_data_litecoin_20210917222254.csv',
                'XMR': 'data/historical_data_monero_20210917220121.csv',
                'ETH': 'data/historical_data_ethereum_20210917220037.csv'}

if __name__ == "__main__":
    for name, data in data_sources.items():
        for graph_type in ['log', 'non_log']:
            # Calculate returns and supply changes
            test = pd.read_csv(data)

            # Preprocess
            test.columns = [c.lower().replace(' ', '_') for c in test.columns]
            test.sort_values('date', ascending=True, inplace=True)
            test['supply_pct'] = test.circulating_supply.pct_change() * 100
            test['closing_return'] = test['price_(close)'].pct_change() * 100
            test.dropna(inplace=True)
            test.reset_index(drop=True, inplace=True)
            test.date = test.date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

            df_day = test[['date', 'supply_pct', 'closing_return']]
            df_day.set_index('date', drop=True, inplace=True)

            plt.figure(figsize=(12, 5))
            plt.title(f'% Change in circulating supply vs. Closing price return for {name}')

            ax1 = df_day.supply_pct.plot(color='blue', grid=True, label='Circulating Supply')
            ax2 = df_day.closing_return.plot(color='green', grid=True, secondary_y=True, label='Return')

            if graph_type == 'log':
                ax1.set_yscale("log")

            h1, l1 = ax1.get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()

            plt.legend(h1 + h2, l1 + l2, loc=2)
            ax1.legend(loc=2)
            ax2.legend(loc=1)
            ax1.set_xlabel('Date')
            if graph_type == 'log':
                ax1.set_ylabel('Log(Supply change %)', color='b')
            else:
                ax1.set_ylabel('Supply change %', color='b')
            ax2.set_ylabel('Return %', color='g')
            plt.show()
