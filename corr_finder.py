import bs4 as bs
import pickle
import requests
import datetime as dt
import pandas as pd
from iexfinance.stocks import get_historical_data
import os

os.environ['IEX_TOKEN'] = 'sk_129d923338c640f99167d869165e8f52'


def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []

    for row in table.findAll('tr')[1:]:

        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        tickers.append(ticker)

    with open('sp500tickers.pickle' , 'wb') as f:
        pickle.dump(tickers, f)

    return tickers


file = open('sp500tickers.pickle', 'rb')
ticker_list = pickle.load(file)
file.close()


start = dt.datetime(2017, 1, 1)
today = dt.datetime.today()
end = [today - dt.timedelta(days = x) for x in range(400)]

def save_daily_data():
    if not 'sp500_daily_data' in os.listdir():
        os.mkdir('../sp500_daily_data')

    for ticker in ticker_list:
        if os.path.exists('sp500_daily_data' + '/' + f'{ticker}.csv'):
            print(f'Already have {ticker}.')

        else:
            data = get_historical_data(f'{ticker}', start, end, output_format = 'pandas')
            data.to_csv('sp500_daily_data' + '/' + f'{ticker}.csv')
            print(f'{ticker} created.')



def find_correlation(datapoint):
    master_df = pd.DataFrame()
    for ticker in ticker_list:

        if ticker in master_df.columns:
            continue

        else:
            ticker_data = pd.read_csv(f'../sp500_daily_data/{ticker}.csv')
            ticker_datapoint = ticker_data[f'{datapoint}']
            master_df[f'{ticker}'] = ticker_datapoint


    master_df.set_index(ticker_data.index, inplace = True)
    master_df = master_df.corr()

    return master_df



def pinpoint_correlations(datapoint):

    combined_data = find_correlation(datapoint)
    pos_list = []
    neg_list = []


    for col in ticker_list:
        current_col = combined_data[f'{col}'].tolist()

        for index,item in enumerate(current_col):
            if .99 <= item < 1:
                pos_list.append([item, [col, ticker_list[index]]])

            elif -1 < item <= -.9:
                neg_list.append([item, [col, ticker_list[index]]])



    print('loop finished')

    for i, item in enumerate(pos_list):
        stock1, stock2 = item[1]

        for item2 in pos_list:

            if item[1] == item2[1]:
                continue

            elif stock1 and stock2 in item2[1]:
                del pos_list[i]
                break

    for i, item in enumerate(neg_list):
        stock1, stock2 = item[1]

        for item2 in neg_list:

            if item[1] == item2[1]:
                continue

            elif stock1 and stock2 in item2[1]:
                del neg_list[i]
                break

    return pos_list, neg_list


