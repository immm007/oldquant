# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date,timedelta


def draw_cyb_adl(_date=(date.today()-timedelta(365)).strftime('%Y-%m-%d')):
    global cyb_adl
    try:
        if cyb_adl is not None:
            pass
    except NameError:
        cyb_adl = calculate(cybz,cyb_stocks)
    draw(cybz,cyb_adl,_date)
    
def draw_sh_adl(_date=(date.today()-timedelta(365)).strftime('%Y-%m-%d')):
    global sh_adl
    try:
        if sh_adl is not None:
            pass
    except NameError:
        sh_adl = calculate(szzs,sh_stocks)
    draw(szzs,sh_adl,_date)

def draw_sz_adl(_date=(date.today()-timedelta(365)).strftime('%Y-%m-%d')):
    global sz_adl
    try:
        if sz_adl is not None:
            pass
    except NameError:
        sz_adl = calculate(szcz,sz_stocks)
    draw(szcz,sz_adl,_date)

def calculate(zs,stocks):
    ret = {'a':[],'d':[],'diff':[]}
    for _date in zs.index:
        sum_a = 0
        sum_d = 0
        for stock in stocks:
            if _date not in stock.index:
                continue
            else:
                if stock['涨跌额'][_date] > 0:
                    sum_a += 1
                elif stock['涨跌额'][_date] < 0:
                    sum_d +=1
        ret['a'].append(sum_a)
        ret['d'].append(sum_d)
        ret['diff'].append(sum_a-sum_d)
    return pd.DataFrame(ret,index=zs.index)

def draw(zs,adl,_date):
    diff = adl['diff'].cumsum()
    plt.subplot(2,1,1)
    plt.plot(zs['收盘价'][_date:])
    plt.subplot(2,1,2)
    plt.plot(diff[_date:])
    plt.show()