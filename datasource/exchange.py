import requests
from datasource import utils
import xlrd
import os

def getAllSHCodes():
    url = "http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1"
    header = {
        "Referer": 'http://www.sse.com.cn/assortment/stock/list/share/'
    }
    res = requests.get(url, headers=header)
    res.raise_for_status()
    h = utils.CSVHelper(res.text)
    next(h)
    return [row[0:6] for row in h]


def getAllSZCodes():
    url = "http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110&TABKEY=tab1&random=0.2335568399319603"
    res = requests.get(url)
    res.raise_for_status()
    with open('tmp.xlsx', 'wb') as f:
        f.write(res.content)
    wb = xlrd.open_workbook('tmp.xlsx')
    sheet = wb.sheet_by_index(0)
    ret = []
    for i in range(1, sheet.nrows):
        ret.append(sheet.row(i)[0].value)
    os.remove('tmp.xlsx')
    return ret
