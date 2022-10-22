import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import os
import datetime as dt
from mplfinance._utils import _construct_candlestick_collections
from make_candles import construct_candles


def night_space(night_length = 60):

    night = pd.DataFrame({'label' : np.zeros(night_length).tolist(),
            'marketOpen': np.zeros(night_length).tolist(),
            'marketHigh': np.zeros(night_length).tolist(),
            'marketLow': np.zeros(night_length).tolist(),
            'marketClose': np.zeros(night_length).tolist(),
            'marketVolume': np.zeros(night_length).tolist()})


    return night


def prepare_data(symbol):

    datelist = os.listdir(f'{symbol}_intraday_data')

    dates = []
    master_df = pd.DataFrame()

    if f'{symbol}_vis_data.csv' not in os.listdir():

        for day in datelist:

            current_data = pd.read_csv(f'{symbol}_intraday_data/{day}')
            night = night_space()

            if not len(current_data):
                master_df = master_df.append(night, ignore_index = True)
                dates += [day] * len(night)

            else:
                current_data = current_data[['label', 'marketOpen', 'marketHigh', 'marketLow', 'marketClose', 'marketVolume']]
                current_data = current_data.append(night, ignore_index = True)
                dates += [day] * len(current_data)
                master_df = master_df.append(current_data, ignore_index = True)


        final_data = pd.DataFrame({'Dates' : dates,
                                   'Times' : master_df['label'],
                                   'Open' : master_df['marketOpen'],
                                   'High' : master_df['marketHigh'],
                                   'Low' : master_df['marketLow'],
                                   'Close' : master_df['marketClose'],
                                   'Volume' : master_df['marketVolume']})

        final_data.to_csv(f'{symbol}_vis_data.csv')

        return final_data

    else:
        print('Already have data.')
        df = pd.read_csv(f'{symbol}_vis_data.csv')

        return df
    # final_data = [master_df['label'], master_df['marketOpen'], master_df['marketHigh'], master_df['marketLow'],
    #               master_df['marketClose'], master_df['marketVolume']]

data = prepare_data('AMD')
print(data.head())
data = data.loc[:,'Times':]
times = data['Times'].tolist()
opens = data['Open'].tolist()
highs = data['High'].tolist()
lows = data['Low'].tolist()
closes = data['Close'].tolist()
df = construct_candles(times, opens, highs, lows, closes)

for i in [times, opens, highs ,lows, closes]:
    print(len(i))

def visualize(symbol, trade_list):

    data = prepare_data(symbol)
    dates = data['Dates']
    times = data['Times']
    ohlc = data.loc[:, 'Open':]

    new_candle_reference = np.arange(len(times))

    total_ohlc = pd.DataFrame(ohlc.iloc[0, :]).transpose()
    init_plot = True
    time_series = []

    for index, time in enumerate(ohlc):
        current_time = times[index]
        time_series.append(pd.Index([current_time]))
        time_series = ['12:00:00' if c == '0.0' else c for c in time_series]
        time_series = pd.DatetimeIndex(time_series)
        total_ohlc.index = time_series

        if init_plot:
            my_plot = mpf.plot(total_ohlc, type = 'candle')

            init = False

        if index == 0:
            continue

        current_ohlc = pd.DataFrame(ohlc.iloc[index,:]).transpose()
        total_ohlc.iloc[-1, 0] = current_ohlc.iloc[0, 0]

        if index < 250:

            if current_time[-1] == '0' or current_time[-1] == '5':

                total_ohlc = total_ohlc.append(current_ohlc, ignore_index = True)

            else:

                if current_ohlc.iloc[0, 1] > total_ohlc.iloc[-1, 1]:
                    total_ohlc.iloc[-1, 1] = current_ohlc.iloc[0, 1]

                if current_ohlc.iloc[0, 2] > total_ohlc.iloc[-1, 2]:
                    total_ohlc.iloc[-1, 2] = current_ohlc.iloc[0, 2]

                if current_ohlc.iloc[0, 3] > total_ohlc.iloc[-1, 3]:
                    total_ohlc.iloc[-1, 3] = current_ohlc.iloc[0, 3]

                if current_ohlc.iloc[0, 4] > total_ohlc.iloc[-1, 4]:
                    total_ohlc.iloc[-1, 4] = current_ohlc.iloc[0, 4]

                if current_ohlc.iloc[0, 5] > total_ohlc.iloc[-1, 5]:
                    total_ohlc.iloc[-1, 5] = current_ohlc.iloc[0, 5]

        else:

            if current_time[-1] == '0' or current_time[-1] == '5':

                total_ohlc = total_ohlc.append(current_ohlc, ignore_index=True)
                total_ohlc.drop(0, axis = 0, inplace = True)

            else:

                if current_ohlc.iloc[0, 1] > total_ohlc.iloc[-1, 1]:
                    total_ohlc.iloc[-1, 1] = current_ohlc.iloc[0, 1]

                if current_ohlc.iloc[0, 2] > total_ohlc.iloc[-1, 2]:
                    total_ohlc.iloc[-1, 2] = current_ohlc.iloc[0, 2]

                if current_ohlc.iloc[0, 3] > total_ohlc.iloc[-1, 3]:
                    total_ohlc.iloc[-1, 3] = current_ohlc.iloc[0, 3]

                if current_ohlc.iloc[0, 4] > total_ohlc.iloc[-1, 4]:
                    total_ohlc.iloc[-1, 4] = current_ohlc.iloc[0, 4]

                if current_ohlc.iloc[0, 5] > total_ohlc.iloc[-1, 5]:
                    total_ohlc.iloc[-1, 5] = current_ohlc.iloc[0, 5]

        #trade info
        # current_trade = trades[0]
        # trade_date = current_trade[0]
        # trade_time = current_trade[1]
        #
        # if current_date == trade_date and current_time == trade_time:
        #     plt.scatter(trade_time, trade_price)


        # my_plot.clear()
        my_plot = mpf.plot(current_ohlc, type = 'candle')
        my_plot.grid()
        my_plot.title(symbol)
        my_plot.xlabel('Time')
        my_plot.ylabel('Price')

        my_plot.show()

