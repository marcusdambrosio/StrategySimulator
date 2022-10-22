import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np
from build_line_data import line_data
from BuildTradeData import give_trade_data
import pandas as pd
from matplotlib import style


def make_ticks(ticks, labels, freq = 5):

    new_ticks, new_labels = [], []
    for i, item in enumerate(ticks):
        if i%freq == 0:
            new_ticks.append(item)
            new_labels.append(labels[i])

    #     if labels[i] == 'Market Closed':
    #         mkt_closed_list.append([i, i + 30])
    #
    #
    # for pair in mkt_closed_list:
    #     plt.axvspan(pair[0], pair[1], alpha = .5)

    plt.xticks(new_ticks, new_labels, rotation = 60 )
    print('Ticks and fill done.')

def graph(pair, order_diff, close_diff):
    stock1 = pair[0]
    stock2 = pair[0]

    closes1, times1, ind1 = line_data(stock1)
    closes2, times2, ind2 = line_data(stock2)
    print('line data finished')
    ######
    longs1, longs2, shorts1, shorts2 = give_trade_data(pair, order_diff, close_diff)
    print('trade data finished')
    # cost1, cost2, side1, trade_time = give_trade_data(pair, order_diff, close_diff)
    #
    # data = pd.DataFrame({'cost1' : cost1,
    #                      'cost2' : cost2,
    #                      'side1' : side1,
    #                      'trade time' : trade_time})
    #
    # longs1 = pd.DataFrame()
    # shorts1 = pd.DataFrame()
    # longs2 = pd.DataFrame()
    # shorts2 = pd.DataFrame()
    #
    #
    # for row in data.iterrows():
    #     if row['side1'] == 'BUY':
    #         longs1.append({'cost' : row['cost1'],
    #                        'time' : row['trade time']})
    #         shorts2.append({'cost2' : row['cost2'],
    #                         'time' : row['trade time']})
    #
    #     else:
    #         longs2.append({'cost': row['cost2'],
    #                        'time': row['trade time']})
    #         shorts1.append({'cost2': row['cost1'],
    #                         'time': row['trade time']})


    fig, ax = plt.subplots(figsize = [ 10,  5])
    plt.plot(times1, closes1, linewidth=2, color = 'black', label = stock1)
    plt.plot(times2, closes2, linewidth=2, color = 'grey', label = stock2)

    plt.scatter(longs1['average cost'].tolist(), longs1['time'].tolist(), color='Green', linewidths=5, marker='o', label=stock1)
    plt.scatter(longs2['average cost'].tolist(), longs2['time'].tolist(), color='Green', linewidths=5, label=stock2)
    plt.scatter(shorts1['average cost'].tolist(), shorts1['time'].tolist(), color='Red', linewidths=5, marker='o', label=stock1)
    plt.scatter(shorts2['average cost'].tolist(), shorts2['time'].tolist(), color='Red', linewidths=5, label=stock2)

#####

#####
    make_ticks(ind1, times1, freq=30)
    plt.grid()

    slider_pos = plt.axes([.2, .95, .65, .03])

    slider = Slider(slider_pos, 'Time', ind1[0], ind1[-1])

    ax.axis([0, 180, closes1[0] - .75, closes1[0] + .75])


    shift = 20

    forward_ax = plt.axes([.9, .9, .07, .05])
    forward = Button(forward_ax, 'Next', color='Green')


    backward_ax = plt.axes([.03, .9, .07, .05])
    backward = Button(backward_ax, 'Back', color='Red')


    plt.show()

    #subplots
    # ax[0].scatter(longs1['cost'].tolist(), longs1['time'].tolist(), color='Green', linewidths=5, marker='o',
    #             label=stock1)
    # ax[1].scatter(longs2['cost'].tolist(), longs2['time'].tolist(), color='Green', linewidths=5, label=stock2)
    # ax[0].scatter(shorts1['cost'].tolist(), shorts1['time'].tolist(), color='Red', linewidths=5, marker='o',
    #             label=stock1)
    # ax[1].scatter(shorts2['cost'].tolist(), shorts2['time'].tolist(), color='Red', linewidths=5, label=stock2)
    #

#
#
# closes, times, ind = line_data('GOOG')
#
# mkt_closed_list = []
#
# fig, ax = plt.subplots(figsize = [10, 5])
# plt.plot(ind, closes, linewidth= 2, color = 'Black')
#

graph(['GOOG', 'GOOGL'], .01, .003)



# make_ticks(ind, times, freq = 30)
# plt.grid()
#
# slider_pos = plt.axes([.2, .95, .65, .03])
#
# slider = Slider(slider_pos, 'Time', ind[0], ind[-1])
# ax.axis([0, 180, closes[0]-.75, closes[0]+.75])

def update(val):
    pos = slider.val
    y_ax = int(np.floor(pos))

    if y_ax < 180:
        avg = np.mean(closes1[:y_ax])

    else:
        avg = np.mean(closes1[y_ax-90:y_ax+90])
    ax.axis([pos, pos+180, avg + .75, avg - .75])
    fig.canvas.draw_idle()
slider.on_changed(update)
shift = 20
#
# slider.on_changed(update)
#
# shift = 20

def click_forward(click):
    slider.val += shift
    update(slider.val)

def click_backward(click):
    slider.val -= shift
    update(slider.val)

forward.on_clicked(click_forward)
backward.on_clicked(click_backward)
#
# forward_ax = plt.axes([.9, .9, .07, .05])
# forward = Button(forward_ax, 'Next', color = 'Green')
# forward.on_clicked(click_forward)
#
# backward_ax = plt.axes([.03, .9, .07, .05])
# backward = Button(backward_ax, 'Back', color = 'Red')
# backward.on_clicked(click_backward)
#
# plt.show()

