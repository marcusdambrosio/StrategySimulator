import pandas as pd
import os
import numpy as np
import datetime as dt
from getting_intraday_data import get_data
from corr_finder import pinpoint_correlations
import time
from TwoStockCorr import find_correlation, load_data
import sys

df = pd.DataFrame({'a':[1,2,3], 'b':[5,6,7]})
empty = pd.DataFrame()
df = df.append(df, ignore_index= True)





def pairs_trades(ticker1, ticker2, order_diff, close_diff, testing = False):

    data1 = load_data(ticker1)
    data2 = load_data(ticker2)

    data1 = data1[['date', 'label', 'marketAverage', 'marketVolume', 'marketChangeOverTime']]
    data2 = data2[['date', 'label', 'marketAverage', 'marketVolume', 'marketChangeOverTime']]

    data1.reset_index(inplace = True)
    data2.reset_index(inplace = True)

    print('done getting data')
    trade_information = pd.DataFrame()
    pos = False
    init_dates = True
    slippage = .02


    for row1 in data1.iterrows():

    #Formatting row data
        index = row1[0]

        if index%5000 == 0:
            print(index)

        try:
          curr_data1 = row1[-1]
          curr_data2 = data2.loc[index, :]




#FIGURE THIS OUT
        except:
            print(row)
            sys.exit('broken')

        current_date = curr_data1['date']

        #SCALER MANAGEMENT
        if init_dates:
            old_date = curr_data1['date']
            scaler1 = curr_data1['marketAverage']
            scaler2 = curr_data2['marketAverage']

            init_dates = False

        if old_date != current_date:
            scaler1 = curr_data1['marketAverage']
            scaler2 = curr_data2['marketAverage']
            old_date = current_date

        scaled_price1 = curr_data1['marketAverage'] / scaler1
        scaled_price2 = curr_data2['marketAverage'] / scaler2

        #OPENING POSITIONS



        if not pos:

            if np.abs(scaled_price1 - scaled_price2) > order_diff:

                side1 = 'BUY' if scaled_price1 < scaled_price2 else 'SELL'
                side2 = 'BUY' if side1 == 'SELL' else 'SELL'

                position1 = np.floor(100000 / curr_data1['marketAverage'])
                position2 = np.floor(100000 / curr_data2['marketAverage'])

                if side1 == 'SELL':
                    pos = True
                    position1 = -position1

                #CANT STORE DATA AS LISTS 
                    trade = {'date' : [current_date] * 2,
                             'time' : [curr_data1['label']] * 2,
                             'symbol' : [ticker1, ticker2],
                             'side' : [side1, side2],
                             'position' : [position1, position2],
                             'average cost' : [curr_data1['marketAverage'] - slippage, curr_data2['marketAverage'] + slippage],
                             'total cost' : np.array([position1, position2]) * np.array([curr_data1['marketAverage'] - slippage, curr_data2['marketAverage'] + slippage])}

                    trade_information = trade_information.append(pd.DataFrame(trade), ignore_index = True)

                else:
                    pos = True
                    position2 = -position2

                    trade = {'date': [current_date] * 2,
                             'time': [curr_data1['label']] * 2,
                             'symbol': [ticker1, ticker2],
                             'side': [side1, side2],
                             'position': [position1, position2],
                             'average cost': [curr_data1['marketAverage'] + slippage, curr_data2['marketAverage'] - slippage],
                             'total cost' : np.array([position1, position2]) * np.array([curr_data1['marketAverage'] - slippage, curr_data2['marketAverage'] + slippage])}

                    trade_information = trade_information.append(pd.DataFrame(trade), ignore_index = True)

        #CLOSING POSITIONS
        else:

            if np.abs(scaled_price1 - scaled_price2) < close_diff:
                #
                # position1 = np.floor(100000 / curr_data1['marketAverage'])
                # position2 = np.floor(100000 / curr_data2['marketAverage'])
                trade = {'date': [current_date] * 2,
                         'time': [curr_data1['label']] * 2,
                         'symbol': [ticker1, ticker2],
                         'side': [side2, side1],
                         'position': [-position1, -position2],
                         'average cost': [curr_data1['marketAverage'] + slippage,
                                          curr_data2['marketAverage'] - slippage],
                         'total cost': -1 * np.array([-position1, -position2]) * np.array(
                             [curr_data1['marketAverage'] - slippage, curr_data2['marketAverage'] + slippage])}

                trade_information = trade_information.append(pd.DataFrame(trade), ignore_index=True)

                # if side1 == 'SELL':
                #     pos = True
                #     position2 = - position2
                #
                #     trade = {'date': [current_date] * 2,
                #              'time': [curr_data1['label']] * 2,
                #              'symbol': [ticker1, ticker2],
                #              'side': [side2, side1],
                #              'position': [position1, position2],
                #              'average cost': [curr_data1['marketAverage'] + slippage, curr_data2['marketAverage'] - slippage],
                #              'total cost': np.array([position1, position2]) * np.array([curr_data1['marketAverage'] - slippage, curr_data2['marketAverage'] + slippage])}
                #
                #     trade_information = trade_information.append(pd.DataFrame(trade), ignore_index = True)
                #
                # else:
                #     pos = True
                #     position1 = -position1
                #
                #     trade = {'date': [current_date] * 2,
                #              'time': [curr_data1['label']] * 2,
                #              'symbol': [ticker1, ticker2],
                #              'side': [side2, side1],
                #              'position': [position1, position2],
                #              'average cost': [curr_data1['marketAverage'] - slippage, curr_data2['marketAverage'] + slippage],
                #              'total cost' : np.array([position1, position2]) * np.array([curr_data1['marketAverage'] - slippage, curr_data2['marketAverage'] + slippage])}
                #
                #     trade_information = trade_information.append(pd.DataFrame(trade), ignore_index = True)

    trade_information.to_csv(f'{ticker1}-{ticker2}_TRADES' + str(order_diff) + str(close_diff) + '.csv')
    return trade_information


#pairs_trades('GOOG', 'GOOGL', .003, .01)

def give_trade_data(pair, order_diff, close_diff):
    stock1, stock2 = pair
    if f'{stock1}-{stock2}_TRADES' + str(order_diff) + str(close_diff) + '.csv' not in os.listdir():

        trade_data = pairs_trades(stock1, stock2, order_diff, close_diff, testing= True)

    else:
        trade_data = pd.read_csv(f'{stock1}-{stock2}_TRADES' + str(order_diff) + str(close_diff) + '.csv')
########
    longs1 = pd.DataFrame()
    shorts1 = pd.DataFrame()
    longs2 = pd.DataFrame()
    shorts2 = pd.DataFrame()

    filtered_data = trade_data[['time', 'symbol', 'side', 'average cost']]

    for row in filtered_data.iterrows():
        row = row[1]

        if row['side'] == 'BUY':

            if row['symbol'] == stock1:
                longs1 = longs1.append(row)
            else:
                longs2 = longs2.append(row)

        else:

            if row['symbol'] == stock1:
                shorts1 = shorts1.append(row)
            else:
                shorts2 = shorts2.append(row)


##############
    # avg_cost = trade_data['average cost'].tolist()
    #
    # avg_cost1 = [c[0] for c in avg_cost]
    # avg_cost2 = [c[1] for c in avg_cost]
    # times = trade_data['time']
    #
    # sides = trade_data['side'].tolist()
    # side1 = [c[0] for c in sides]
    #
    # return avg_cost1, avg_cost2, side1, times

    return longs1, longs2, shorts1, shorts2

def calculate_returns(pair, order_diff = None, close_diff = None):
    stock1, stock2 = pair

    if f'{stock1}-{stock2}_TRADES' + str(order_diff) + str(close_diff) + '.csv' not in os.listdir():

        trade_data = pairs_trades(stock1, stock2, order_diff, close_diff, testing= True)

    else:
        trade_data = pd.read_csv(f'{stock1}-{stock2}_TRADES' + str(order_diff) + str(close_diff) + '.csv')

    pnl = []
    total_costs = trade_data['total cost'].tolist()

    # print('starting calcs')
    # for index in range(len(total_costs)):
    #     print(np.sum(total_costs[:index + 1]))
    #     pnl.append(np.sum(total_costs[:index+1]))
    #
    #
    buys = [c for c in total_costs if 0 < c < -900000]
    sells = [c for c in total_costs if c]
    print(len(buys), len(sells))
    pnl = np.sum(total_costs)
    balance = pnl + 500000
    #
    # date_time = []
    #
    # for i, item in enumerate(trade_data['date']):
    #     time_object = trade_data['time'][i]
    #
    #     if time_object[-2] == 'A':
    #         if len(time_object) < 6:
    #             time_object = time_object[:2] + ':00'
    #
    #         else:
    #             time_object = time_object[:5]
    #
    #     else:
    #         hour = int(time_object[0]) + 12
    #         time_object = str(hour) + ':' + time_object[2:5]
    #     print(time_object)
    #
    #     dt_obj = dt.datetime.strptime(item + ' ' + time_object, '%Y-%m-%d %H:%M')
    #     date_time.append(dt_obj)
    #
    # time_diff = []
    # time_counter = 2
    # while time_counter < len(trade_data):
    #     time_diff.append(date_time[time_counter] - date_time[time_counter - 2])
    #     time_counter += 1

    return np.sum(pnl), np.sum(balance)


pnl, balance = calculate_returns(['GOOG', 'GOOGL'], .003, .01)

print(pnl, balance)