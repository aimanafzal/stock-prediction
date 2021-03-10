from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request
# import urllib.json
import os
# import numpy as np
# import tensorflow as tf
# from sklearn.preprocessing import MinMaxScaler

#ITTGJM6D6TVOWH28

data_source = 'kaggle'
if data_source == 'alphavantage':
    api_key = 'ITTGJM6D6TVOWH28'
    ticker = 'AAL'

    url_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)'
    file_to_save = 'stock_market_data-%s.csv' % ticker
    if not os.path.exists(file_to_save):
        with urllib.request.urlopen(url_string) as url:
            data = json.loads(url.read().decode())

            data = data['Time Series (Daily)']
            df = pd.DataFrame(columns=['Date','low','High','Close','Open'])
            for k,v in data.items():
                date = dt.datetime.strptime(k, '%Y-%m-%d')
                data_row = [date.date(), float(v['3. low']),
                            float(v['2. high']),
                            float(v['4. close']),
                            float(v['1. open'])
                            ]
                df.loc[-1, :] = data_row
                df.index = df.index + 1
        print('Data saved to :%s'%file_to_save)
        df.to_csv(file_to_save)
    else:
        print('File already exists. Loading data from CSV')
        df = pd.read_csv(file_to_save)

else:
    df = pd.read_csv(os.path.join('archive/Stocks', 'hpq.us.txt'), delimiter=',', usecols=['Date', 'Open', 'High', 'Low', 'Close'])
    print('Loaded data from Kaggle repository')