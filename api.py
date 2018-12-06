from datasource import wangyi, utils, exchange
from datetime import datetime, timedelta
import os
import pandas as pd

data_folder = 'E:/quant/data/'

def calculateEndDate():
    now = datetime.now()
    today = now.date()
    stamp = datetime(today.year, today.month, today.day, 16, 30, 0)
    if now < stamp:
        end_date = today-timedelta(1)
    else:
        end_date = today
    return end_date


def downloadSingle(code):
    end_date = calculateEndDate().strftime('%Y%m%d')
    content = wangyi.getDayData(code, '19900101', end_date)
    with open(data_folder+end_date+'-'+'%s.csv' % code, 'w', newline='') as f:
        helper1 = utils.CSVHelper(content)
        f.write(next(helper1))
        helper = utils.WYRCSVHelper(content)
        f.writelines(helper)


def downloadAllWithSkip():
    codes = exchange.getAllSHCodes()
    downloaded_codes = [name[9:15] for name in os.listdir(data_folder)]
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
    end_date = calculateEndDate().strftime('%Y%m%d')
    for code in sh_codes:
        content = wangyi.getDayData(code, '19900101', end_date)
        with open(data_folder+end_date+'-'+'%s.csv' % code, 'w', newline='') as f:
            f.write(content[0:62])
            helper = utils.WYRCSVHelper(content)
            f.writelines(helper)
    for code in sz_codes:
        content = wangyi.getDayData(code, '19900101', end_date)
        with open(data_folder+end_date+'-'+'%s.csv' % code, 'w', newline='') as f:
            f.write(content[0:62])
            helper = utils.WYRCSVHelper(content)
            f.writelines(helper)              

            
def complementAll():
    #todo 还是太慢，10分钟样子
    end_date = calculateEndDate()
    for name in os.listdir(data_folder):
        last_date = datetime.strptime(name[0:8], '%Y%m%d').date()
        code = name[9:15]
        if end_date > last_date:
            path = data_folder + name
            start_date = last_date+timedelta(1)
            end_date = end_date.strftime('%Y%m%d')
            content = wangyi.getDayData(code, start_date.strftime('%Y%m%d'), end_date)
            with open(path, 'a') as f:
                f.writelines(utils.WYRCSVHelper(content))
            os.rename(path, data_folder+end_date+'-'+'%s.csv' % code)


def removeExtra():
    codes1 = exchange.getAllSHCodes()
    codes2 = exchange.getAllSZCodes()
    for name in os.listdir(data_folder):
        code = name[9:15]
        if code not in codes1 and code not in codes2:
            print('remove\t' + name)
            os.remove(data_folder+name)


def removeSpecial():
    names = checkLastDate()
    for name in names:
        print('remove\t' + name)
        os.remove(data_folder+name)


def checkLastDate():
    ret = []
    for name in os.listdir(data_folder):
        date = name[0:8]
        with open(data_folder+name,'r') as f:
            content = f.readlines()
            if content[-1][0:10].replace('-', '') != date:
                ret.append(name)
    return ret


def read(code):
    date = calculateEndDate().strftime('%Y%m%d')
    path = data_folder+date+'-'+'%s.csv' % code
    return pd.read_csv(path, encoding='gbk',index_col=0)


def readAll():
    return [pd.read_csv(data_folder+name,encoding='gbk',index_col=0) for name in os.listdir(data_folder)]
        