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

def draw_zxb_adl(_date=(date.today()-timedelta(365)).strftime('%Y-%m-%d')):
    global zxb_adl
    try:
        if zxb_adl is not None:
            pass
    except NameError:
        zxb_adl = calculate(zxbz,zxb_stocks)
    draw(zxbz,zxb_adl,_date)

def calculate(zs,stocks):
    ret = []
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
        ret.append(sum_a-sum_d)
    return pd.Series(ret,index=zs.index).cumsum()

def draw(zs,adl,_date):
    diff = adl['diff'].cumsum()
    plt.subplot(2,1,1)
    plt.plot(zs['收盘价'][_date:])
    plt.subplot(2,1,2)
    plt.plot(diff[_date:])
    plt.show()

def export():
    s1 = calculate(szzs,sh_stocks)
    s1.name = 'szzs'
    s2 = calculate(szcz,sz_stocks)
    s2.name = 'szcz'
    s3 = calculate(zxbz,zxb_stocks)
    s3.name = 'zxbz'
    s4 = calculate(cybz,cyb_stocks)
    s4.name = 'cybz'
    df = pd.DataFrame([s1,s2,s3,s4]).T
    df.to_csv('adl.csv',index_label='date',na_rep='0.5')
    