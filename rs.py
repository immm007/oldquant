# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date,timedelta


def draw_rs(zs,stock,_date=(date.today()-timedelta(365)).strftime('%Y-%m-%d')):
    zs_zdf = zs['涨跌幅'][_date:]
    zdf = stock['涨跌幅'][zs_zdf.index]
    rs = (zdf - zs_zdf).cumsum()
    plt.subplot(2,1,1)
    plt.plot(stock['收盘价'][zs_zdf.index])
    plt.subplot(2,1,2)
    plt.plot(rs)
    plt.show()


def sort_by_rs(zs,stocks,s_date,e_date=None):
    if e_date is None:
        zs_zdf = zs['涨跌幅'][s_date:]
    else:
        zs_zdf = zs['涨跌幅'][s_date:e_date]
    ret = []
    for stock in stocks:
        zdf = stock['涨跌幅'][zs_zdf.index]
        rs = (zdf - zs_zdf).cumsum()
        rs.name = stock['股票代码'].iloc[0]
        ret.append(rs)
    return pd.DataFrame(ret)
    
            