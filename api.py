from datasource import wangyi, utils, exchange
from datetime import datetime, timedelta, date
import os
import pandas as pd

data_folder = 'E:/quant/data/'


def downloadSingle(code: str,end_date:date=None):
    if end_date is None:
        end_date = date.today()
    content = wangyi.getDayData(code, end_date)
    helper = utils.CSVHelper(content)
    next(helper)
    latest_date = next(helper)[0:10]
    with open(data_folder+latest_date+'-'+'%s.csv' % code, 'w', newline='') as f:
        f.write(content[0:62])
        helper = utils.WYRCSVHelper(content)
        f.writelines(helper)
        
        
def complementDownload():
    codes = exchange.getAllSHCodes()
    downloaded_codes = [name[11:17] for name in os.listdir(data_folder)]
    for code in codes:
        if code in downloaded_codes:
            continue
        downloadSingle(code)
    codes = exchange.getAllSZCodes()
    for code in codes:
        if code in downloaded_codes:
            continue
        downloadSingle(code)


def fastDownloadAll():
    sh_codes = exchange.getAllSHCodes()
    sz_codes = exchange.getAllSZCodes()
    end_date = date.today()
    for code in sh_codes:
        content = wangyi.getDayData(code, end_date)
        helper = utils.CSVHelper(content)
        next(helper)
        latest_date = next(helper)[0:10]
        with open(data_folder+latest_date+'-'+'%s.csv' % code, 'w', newline='') as f:
            f.write(content[0:62])
            helper = utils.WYRCSVHelper(content)
            f.writelines(helper)
    for code in sz_codes:
        content = wangyi.getDayData(code, end_date)
        helper = utils.CSVHelper(content)
        next(helper)
        latest_date = next(helper)[0:10]
        with open(data_folder+latest_date+'-'+'%s.csv' % code, 'w', newline='') as f:
            f.write(content[0:62])
            helper = utils.WYRCSVHelper(content)
            f.writelines(helper)              
            
            
def complementAll():
    end_date = date.today()
    for name in os.listdir(data_folder):
        last_date = datetime.strptime(name[0:10], '%Y-%m-%d').date()
        if end_date > last_date:
            code = name[11:17]    
            start_date = last_date+timedelta(1)
            content = wangyi.getDayData(code, end_date, start_date)
            helper = utils.CSVHelper(content)
            next(helper)
            try:
                latest_date = next(helper)[0:10]
                path = data_folder + name
                with open(path, 'a') as f:
                    f.writelines(utils.WYRCSVHelper(content))
                os.rename(path, data_folder+latest_date+'-'+'%s.csv' % code)
            except StopIteration:
                return


def checkLastDate():
    ret = []
    for name in os.listdir(data_folder):
        lastest_date = name[0:10]
        with open(data_folder+name, 'r') as f:
            content = f.readlines()
            if content[-1][0:10] != lastest_date:
                ret.append(name)
    return ret


def readAll():
    return [pd.read_csv(data_folder+name,encoding='gbk',index_col=0) for name in os.listdir(data_folder)]
