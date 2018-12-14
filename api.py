from datasource import wangyi, utils, exchange
from datetime import datetime, timedelta, date
import os
import pandas as pd


stocks_folder = 'E:/quant/data/stocks/'
indexes_folder = 'E:/quant/data/indexes/'


def downloadSingle(code: str,end_date:date=date.today()):
    content = wangyi.getDayData(code, end_date)
    helper = utils.CSVHelper(content)
    next(helper)
    latest_date = next(helper)[0:10]
    with open(stocks_folder + latest_date + '-' + '%s.csv' % code, 'w', newline='') as f:
        f.write(content[0:62])
        helper = utils.WYRCSVHelper(content,62)
        f.writelines(helper)
        
        
def complementDownloadAll():
    codes = exchange.getAllSHCodes()
    downloaded_codes = [name[11:17] for name in os.listdir(stocks_folder)]
    for code in codes:
        if code in downloaded_codes:
            continue
        downloadSingle(code)
    codes = exchange.getAllSZCodes()
    for code in codes:
        if code in downloaded_codes:
            continue
        downloadSingle(code)


def reDownloadAll():
    sh_codes = exchange.getAllSHCodes()
    sz_codes = exchange.getAllSZCodes()
    end_date = date.today()
    for code in sh_codes:
        content = wangyi.getDayData(code, end_date)
        helper = utils.CSVHelper(content)
        next(helper)
        latest_date = next(helper)[0:10]
        with open(stocks_folder + latest_date + '-' + '%s.csv' % code, 'w', newline='') as f:
            f.write(content[0:62])
            helper = utils.WYRCSVHelper(content,62)
            f.writelines(helper)
    for code in sz_codes:
        content = wangyi.getDayData(code, end_date)
        helper = utils.CSVHelper(content)
        next(helper)
        latest_date = next(helper)[0:10]
        with open(stocks_folder + latest_date + '-' + '%s.csv' % code, 'w', newline='') as f:
            f.write(content[0:62])
            helper = utils.WYRCSVHelper(content,62)
            f.writelines(helper)              
            
            
def complementAll():
    end_date = date.today()
    for name in os.listdir(stocks_folder):
        last_date = datetime.strptime(name[0:10], '%Y-%m-%d').date()
        if end_date > last_date:
            code = name[11:17]    
            start_date = last_date+timedelta(1)
            content = wangyi.getDayData(code, end_date, start_date)
            helper = utils.CSVHelper(content)
            next(helper)
            try:
                latest_date = next(helper)[0:10]
                path = stocks_folder + name
                with open(path, 'a') as f:
                    f.writelines(utils.WYRCSVHelper(content,62))
                os.rename(path, stocks_folder + latest_date + '-' + '%s.csv' % code)
            except StopIteration:
                continue


def downloadIndexes():
    indexes = ['0000001','0000016','0000300',
               '1399001','1399106','1399006','1399102']
    dt = datetime.now()
    _date = dt.date()
    if dt <  datetime(_date.year, _date.month, _date.day,15,30,0):
        _date -= timedelta(1)
    for index in indexes:
        content = wangyi.getIndexData(index, _date)
        with open(indexes_folder+ '%s.csv' % index[1:], 'w', newline='') as f:
            f.write(content[0:48])
            helper = utils.WYRCSVHelper(content,48)
            f.writelines(helper)


def checkLastDate():
    ret = []
    for name in os.listdir(stocks_folder):
        lastest_date = name[0:10]
        with open(stocks_folder + name, 'r') as f:
            content = f.readlines()
            if content[-1][0:10] != lastest_date:
                ret.append(name)
    return ret


def readAllStocks():
    return [pd.read_csv(stocks_folder + name, encoding='gbk', index_col=0,
                        converters={
                                '收盘价':utils.Float,
                                '最高价':utils.Float,
                                '最低价':utils.Float,
                                '开盘价':utils.Float,
                                '前收盘':utils.Float,
                                '涨跌额':utils.Float,
                                '涨跌幅':utils.Float,
                                '换手率':utils.Float,
                                '成交量':utils.Int,
                                '成交金额':utils.Float,
                                '总市值':utils.Float,
                                '流通市值':utils.Float
                                }) for name in os.listdir(stocks_folder)]


def readIndex(code):
    return pd.read_csv(indexes_folder+code+'.csv',encoding='gbk',index_col=0,
                       converters={
                                '收盘价':utils.Float,
                                '最高价':utils.Float,
                                '最低价':utils.Float,
                                '开盘价':utils.Float,
                                '前收盘':utils.Float,
                                '涨跌额':utils.Float,
                                '涨跌幅':utils.Float,
                                '成交量':utils.Int,
                                '成交金额':utils.Float
                               })
