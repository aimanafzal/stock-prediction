from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request
import json
import os

import os.path
from os import path

import numpy as np
# import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler



import iexfinance
from iexfinance.stocks import get_historical_data
from datetime import datetime, date
#
# #ITTGJM6D6TVOWH28
#
data_source = 'kaggle'
data_source = 'alphavantage'
if data_source == 'alphavantage':
    api_key = 'ITTGJM6D6TVOWH28'
    ticker = 'AAL'

    url_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s' %(ticker,api_key)
    file_to_save = 'stock_market_data-%s.csv' % ticker
    with urllib.request.urlopen(url_string) as url:
        try:
            if path.exists('stock_market_data-AAL.csv'):
                df = pd.DataFrame(columns=['Date', 'low', 'High', 'Close', 'Open'])
                df.head()
                plt.figure(figsize=(18, 9))
                plt.plot(range(df.shape[0]), (df['Low'] + df['High']) / 2.0)
                plt.xticks(range(0, df.shape[0], 500), df['Date'].loc[::500], rotation=45)
                plt.xlabel('Date', fontsize=18)
                plt.ylabel('Mid Price', fontsize=18)
                plt.show()

                # Calculating mid prices from the highest and lowest
                high_prices = df.loc[:,'High'].as_matrix()
                low_prices = df.loc[:,'Low'].as_matrix()
                mid_prices = (high_prices + low_prices)/2.0

                # Splitting training data and test data
                train_data = mid_prices[:11000]
                test_data = mid_prices[11000:]

                #Scaling data to be between 0 and 1 only
                scaler = MinMaxScaler()
                train_data = train_data.reshape(-1,1)
                test_data = test_data.reshape(-1,1)
            else:
                data = json.loads(url.read().decode())
                data = data['Time Series (Daily)']
                df = pd.DataFrame(columns=['Date', 'low', 'High', 'Close', 'Open'])
                for k, v in data.items():
                    date = dt.datetime.strptime(k, '%Y-%m-%d')
                    data_row = [date.date(), float(v['3. low']),
                                float(v['2. high']),
                                float(v['4. close']),
                                float(v['1. open'])
                                ]
                    df.loc[-1, :] = data_row
                    df.index = df.index + 1
                print('Data saved to :%s' % file_to_save)
                df.to_csv(file_to_save)
                df.sort_values('Date')
                df.head()
        except Exception as Error:
            print (Error)

    # else:
    #     print('File already exists. Loading data from CSV')
    #     df = pd.read_csv(file_to_save)

else:
    df = pd.read_csv(os.path.join('archive/Stocks', 'hpq.us.txt'), delimiter=',', usecols=['Date', 'Open', 'High', 'Low', 'Close'])
    print('Loaded data from Kaggle repository')
    df = df.sort_values('Date')
    df.head()
