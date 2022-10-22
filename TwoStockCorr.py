import pandas as pd
from getting_intraday_data import get_data
import os
import numpy as np
import math
import pickle
from corr_finder import pinpoint_correlations
import time

os.environ['IEX_TOKEN'] = 'sk_129d923338c640f99167d869165e8f52'


def load_data(stock):

    get_data(stock)
    dates =  os.listdir(f'{stock}_intraday_data')

    master_df = pd.DataFrame()
    drop_list1 = []
    drop_list2 = []

    for day in dates:

        df = pd.read_csv(f'{stock}_intraday_data' + '/' + f'{day}')

        if len(df):
            try:
                df = df[['date', 'label', 'marketAverage', 'marketVolume', 'marketChangeOverTime']]
                master_df = master_df.append(df, ignore_index = True)
            except:
                print(day, stock)
    master_df.dropna(axis = 0, inplace = True)

    return master_df


def find_correlation(data1, data2, datapoint = 'close'):

    for dataset in [data1, data2]:

        if dataset is data1:
            master1 = []
            ind_list1 = []

            for index, day in enumerate(dataset):

                if len(day[f'{datapoint}']) != 390:
                    ind_list1.append((day['date'])[0])
                    continue

                else:
                    master1.append([index, day[f'{datapoint}'].tolist()])


        elif dataset is data2:
            master2 = []
            ind_list2 = []

            for index, day in enumerate(dataset):

                if len(day[f'{datapoint}']) != 390:
                    ind_list2.append((day['date'])[0])
                    continue
                #
                # elif (day['date'])[0] in ind_list1:
                #     continue

                else:
                    master2.append([index, day[f'{datapoint}'].tolist()])

        else:
            print('Data not found')


    one_dates = [c[0] for c in master1]
    two_dates = [c[0] for c in master2]

    new_master1 = []
    new_master2 = []

    for item in master1:

        if item[0] in two_dates and item[0] in one_dates:
            curr_list = item[1]

            for i, val in enumerate(item[1]):

                if math.isnan(val):

                    try:
                        curr_list[i] = (curr_list[i-1] + curr_list[i+1]) / 2

                    except:
                        curr_list[i] = curr_list[i-1]

            new_master1 += curr_list

    for item in master2:

        if item[0] in two_dates and item[0] in one_dates:
            curr_list = item[1]

            for i, val in enumerate(item[1]):

                if math.isnan(val):
                    try:
                        curr_list[i] = (curr_list[i - 1] + curr_list[i + 1]) / 2
                    except:
                        curr_list[i] = curr_list[i-1]

            new_master2 += curr_list


    # corr_matrix = np.corrcoef(new_master1,new_master2)

    return new_master1, new_master2



def pairs_research(ticker1, ticker2, order_diff, close_diff):

    # data1 , data2 = find_correlation(load_data(ticker1), load_data(ticker2))

    pnl = 0
    buypoints = []
    sellpoints = []

    min_counter = 0
    pos = False

    order_count = 0

    data1 = np.array(ticker1)
    data2 = np.array(ticker2) 
    scaled_data1 = data1 / data1[0]
    scaled_data2 = data2 / data2[0]

    low_stock_pos = 0

    for i, item in enumerate(scaled_data1):

        if not pos:

            if np.abs(item - scaled_data2[i]) > order_diff:

                if item > scaled_data2[i]:
                    type = 'short1'

                    if data1[i] < data2[i]:
                        second_pos = data2[i] / data1[i]
                        pnl += second_pos * data1[i]
                        pnl -= data2[i]
                        pos = True
                        order_count += 1
                        bigger = '2 bigger'

                    else:
                        second_pos = data1[i] / data2[i]
                        pnl += data1[i]
                        pnl -= second_pos * data2[i]
                        pos = True
                        order_count += 1
                        bigger = '1 bigger'

                else:
                    type = 'short2'

                    if data1[i] < data2[i]:
                        second_pos = data2[i] / data1[i]
                        pnl -= second_pos * data1[i]
                        pnl += data2[i]
                        pos = True
                        order_count += 1
                        bigger = '2 bigger'

                    else:
                        second_pos = data1[i] / data2[i]
                        pnl -= data1[i]
                        pnl += second_pos * data2[i]
                        pos = True
                        order_count += 1
                        bigger = '1 bigger'

        else:

            if np.abs(item - scaled_data2[i]) < close_diff:

                if type == 'short1':

                    if bigger == '2 bigger':

                        pnl -= second_pos * data1[i]
                        pnl += data2[i]
                        pos = False

                    else:

                        pnl -= data1[i]
                        pnl += second_pos * data2[i]
                        pos = False

                else:
                    if bigger == '2 bigger':

                        pnl += second_pos * data1[i]
                        pnl -= data2[i]
                        pos = False

                    else:

                        pnl += data1[i]
                        pnl -= second_pos * data2[i]
                        pos = False



    if pos:

        if type == 'short1':

            if bigger == '2 bigger':

                pnl -= second_pos * data1[-1]
                pnl += data2[-1]
                pos = False

            else:

                pnl -= data1[-1]
                pnl += second_pos * data2[-1]
                pos = False



        else:
            if bigger == '2 bigger':

                pnl += second_pos * data1[-1]
                pnl -= data2[-1]
                pos = False

            else:

                pnl += data1[-1]
                pnl -= second_pos * data2[-1]
                pos = False


    if data1[0] > data2[0]:
        pct_pnl = pnl / data1[0] * 100

    else:
        pct_pnl = pnl / data2[0] * 100

    return [pnl, pct_pnl, order_count, order_diff, close_diff]



#choose order params

diffone = np.linspace(.01, .05, 10)
difftwo = np.linspace(0, .02, 5)




reset = False

def mass_sim():
    pos_list, neg_list = pinpoint_correlations('close')
    print(pos_list)

    if reset:
        PARAMS = pd.DataFrame(columns=['pnl', 'pnl %', 'order count', 'order diff', 'close diff', 'correlation', 'pair'])

        for pair in pos_list:
            print(pair)
            ticker1, ticker2 = pair[1]
            loaded1, loaded2 = find_correlation(load_data(ticker1), load_data(ticker2))
            print(f'{pair[1]} data collected')

            for a in diffone:

                for b in difftwo:
                    if b >= a:
                        continue

                    results = pairs_research(loaded1, loaded2, a , b)

                    new_row = {'pnl' : results[0],
                               'pnl %' : results[1],
                               'order count' : results[2],
                               'order diff' : results[3],
                               'close diff' : results[4],
                               'correlation' : pair[0],
                               'pair' : pair[1]}

                    PARAMS = PARAMS.append(new_row, ignore_index = True)

                    print(a, b, 'tested')


            print(f'{pair[1]} fully tested')

        PARAMS.to_csv('MASS_SIM_FILE2.csv')
        print('file saved')



# bigdata = pd.read_csv('MASS_SIM_FILE2.csv')
#


def unique(list1):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


def filter_data(show_all = False):

    bigdata = pd.read_csv('MASS_SIM_FILE2.csv')

    filtered_data = pd.DataFrame()

    order_count = bigdata['order count']

    for i , item in enumerate(order_count):
        if item < 30:
            bigdata = bigdata.drop(i, axis = 0)

    bigdata.reset_index(inplace = True)

    if show_all:
        for row in bigdata.iterrows():
            print(row)

    pairs = bigdata['pair'].tolist()
    unique_pairs = unique(pairs)

    for pair in unique_pairs:
        pair_best = [0 , 0]

        for row in bigdata.iterrows():
            index = row[0]
            row = row[1]


            if row[-1] == pair:

                if row[1] > pair_best[0]:

                    pair_best = [row[3], index]


        # PNL FILTERING

        if pair_best[0] > 50:
            filtered_data = filtered_data.append(bigdata.iloc[pair_best[1], :])

        else:
            print(f'Profit of {pair_best[0]} insufficient.')

    #FILTERIU
    return filtered_data

# fdata = filter_data()
#
# fdata.to_csv('FILTERED_SIM_DATA2.csv')
#
