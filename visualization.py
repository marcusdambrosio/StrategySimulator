import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance
import os
from mplfinance._utils import _construct_candlestick_collections

# def night_space(model_df, night_length = 60):
#     column_count = len(model_df.columns.tolist())
#     night = {}
#
#     for column in model_df.columns.tolist():
#         night[f'{column}'] = np.zeros(night_length)
#
#     return night

def night_space(night_length = 60):

    night = {'Open': np.zeros(night_length),
            'High': np.zeros(night_length),
            'Low': np.zeros(night_length),
            'Close': np.zeros(night_length),
            'Volume': np.zeros(night_length)}

    return night

df = night_space()
def prepare_data(trades):
    symbol = trades[f'{symbol}'][0]
    datelist = os.listdir(f'{symbol}_intraday_data')

    master_df = pd.Dataframe()

    for day in datelist:
        current_data = pd.load_csv(f'{symbol}_intraday_data/{day}')
        current_data.append(night_space(current_data), inplace=True)

        master_df.append(current_data, inplace=True)

    final_data = [master_df['label'], master_df['marketOpen'], master_df['marketHigh'], master_df['marketLow'],
                  master_df['marketClose'], master_df['marketVolume']]
    dates = master_df['date']

    return final_data, dates, trades


def visualize(symbol, trade_list):

    ohlc, dates, trades = prepare_data(trade_list)

    my_plot = plt.figure()
    ax1 = my_plot.add_sublot([1,1,1])

    new_candle_reference = np.arange(len(ohlc))
    old_ohlc = [col[0] for col in ohlc]
    total_ohlc = old_ohlc

    for index, time in enumerate(ohlc):

        current_ohlc = [col[index] for col in ohlc]

        if index < 250:

            if new_candle_reference%5 == 0:

                for i, item in enumerate(current_ohlc):
                    total_ohlc[i] = total_ohlc[i].append(item)

            else:

                if current_ohlc[1] > old_ohlc[1]:
                    old_ohlc[1] = current_ohlc[1]

                if current_ohlc[2] > old_ohlc[2]:
                    old_ohlc[2] = current_ohlc[2]

                if current_ohlc[3] < old_ohlc[3]:
                    olc_ohlc[3] = current_ohlc[3]

                if current_ohlc[4] < old_ohlc[4]:
                    old_ohlc[4] = current_ohlc[4]

                if current_ohlc[5] > old_ohlc[5]:
                    old_ohlc[5] = current_ohlc[5]

                total_ohlc[-1] = old_ohlc

        else:

            if new_candle_reference % 5 == 0:

                for i, item in enumerate(current_ohlc):
                    current_col = total_ohlc[i]
                    del current_col[0]
                    current_col.append(item)

                    total_ohlc[i] = current_col

            else:

                if current_ohlc[1] > old_ohlc[1]:
                    old_ohlc[1] = current_ohlc[1]

                if current_ohlc[2] > old_ohlc[2]:
                    old_ohlc[2] = current_ohlc[2]

                if current_ohlc[3] < old_ohlc[3]:
                    olc_ohlc[3] = current_ohlc[3]

                if current_ohlc[4] < old_ohlc[4]:
                    old_ohlc[4] = current_ohlc[4]

                if current_ohlc[5] > old_ohlc[5]:
                    old_ohlc[5] = current_ohlc[5]

                total_ohlc[-1] = old_ohlc

        #trade info
        current_trade = trades[0]
        trade_date = current_trade[0]
        trade_time = current_trade[1]

        if current_date == trade_date and current_time == trade_time:
            plt.scatter(trade_time, trade_price)
        ax1.clear()

        candlestick_ohlc(ax1, current_ohlc, colorup='#77d879', colordown='#db3f3f')
        ax1.grid()
        ax1.title(symbol)
        ax1.xlabel('Time')
        ax1.ylabel('Price')

        ax1.show()
