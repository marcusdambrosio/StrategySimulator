import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import datetime as dt
import os
import math
import numpy as np


midnight = dt.time(12, 00, 00)
midnight = 'Market Closed'

def prepare_data(symbol):

    datelist = os.listdir(f'{symbol}_intraday_data')

    init_price = True
    dates = []
    master_list = []
    times = []

    if f'{symbol}_vis_data.csv' not in os.listdir():

        for day in datelist:

            current_data = pd.read_csv(f'{symbol}_intraday_data/{day}')
            try:
                current_data = current_data[['label', 'marketClose']]
                current_data.dropna(axis=0, inplace=True)
            except:
                current_data = []



            if not len(current_data):

                if not len(master_list):
                    continue

                master_list += [master_list[-1]] * 30
                dates += [day[:-3]] * 30
                times += [midnight] * 30

            else:
                closes = current_data['marketClose'].tolist()
                curr_times = current_data['label'].tolist()

                if not len(master_list):
                    master_list += (closes + [closes[-1]] * 30)
                    dates += [day] * (len(curr_times) + 30)
                    times += (curr_times + [midnight] * 30)

                else:
                    master_list += (closes + [closes[-1]] * 30)
                    dates += [day] * (len(curr_times) + 30)
                    times += (curr_times + [midnight] * 30)

        master_df = pd.DataFrame({'dates' : dates,
                                  'times' : times,
                                  'closes' : master_list})
        master_df.to_csv(f'{symbol}_vis_data.csv')

    else:
        print(f'Already have data for {symbol}')
        master_df = pd.read_csv(f'{symbol}_vis_data.csv')

    return master_df

def line_data(ticker):
    data = prepare_data(ticker)
    closes = data['closes'].tolist()
    times = data['times'].tolist()
    ind = data.index.tolist()

    times = [str(c) for c in times]

    return [closes,times,ind]
