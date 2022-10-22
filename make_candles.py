from mplfinance._utils import _get_mpfstyle, _updown_colors, mcolors, LineCollection
from mplfinance.plotting import _valid_plot_kwargs
from mplfinance._arg_validators import _process_kwargs
from mplfinance._widths import _determine_width_config

def construct_candles(dates, opens, highs, lows, closes, marketcolors=None, config=None, **kwargs):
    """Represent the open, close as a bar line and high low range as a
    vertical line.

    NOTE: this code assumes if any value open, low, high, close is
    missing they all are missing


    Parameters
    ----------
    opens : sequence
        sequence of opening values
    highs : sequence
        sequence of high values
    lows : sequence
        sequence of low values
    closes : sequence
        sequence of closing values
    marketcolors : dict of colors: up, down, edge, wick, alpha
    alpha : float
        bar transparency

    Returns
    -------
    ret : list
        (lineCollection, barCollection)
    """
    xdates = dates
    config = _process_kwargs(kwargs, _valid_plot_kwargs())
    config['_width_config'] = _determine_width_config(xdates, config)

    if marketcolors is None:
        marketcolors = _get_mpfstyle('classic')['marketcolors']
        # print('default market colors:',marketcolors)

    datalen = len(dates)

    # avg_dist_between_points = (dates[-1] - dates[0]) / float(datalen)

    delta = config['_width_config']['candle_width'] / 2.0

    barVerts = [((date - delta, open),
                 (date - delta, close),
                 (date + delta, close),
                 (date + delta, open))
                for date, open, close in zip(dates, opens, closes)]

    rangeSegLow = [((date, low), (date, min(open, close)))
                   for date, low, open, close in zip(dates, lows, opens, closes)]

    rangeSegHigh = [((date, high), (date, max(open, close)))
                    for date, high, open, close in zip(dates, highs, opens, closes)]

    rangeSegments = rangeSegLow + rangeSegHigh

    alpha = marketcolors['alpha']

    uc = mcolors.to_rgba(marketcolors['candle']['up'], alpha)
    dc = mcolors.to_rgba(marketcolors['candle']['down'], alpha)
    colors = _updown_colors(uc, dc, opens, closes)

    uc = mcolors.to_rgba(marketcolors['edge']['up'], 1.0)
    dc = mcolors.to_rgba(marketcolors['edge']['down'], 1.0)
    edgecolor = _updown_colors(uc, dc, opens, closes)

    uc = mcolors.to_rgba(marketcolors['wick']['up'], 1.0)
    dc = mcolors.to_rgba(marketcolors['wick']['down'], 1.0)
    wickcolor = _updown_colors(uc, dc, opens, closes)

    lw = config['_width_config']['candle_linewidth']

    rangeCollection = LineCollection(rangeSegments,
                                     colors=wickcolor,
                                     linewidths=lw,
                                     )

    barCollection = PolyCollection(barVerts,
                                   facecolors=colors,
                                   edgecolors=edgecolor,
                                   linewidths=lw
                                   )

    return [rangeCollection, barCollection]