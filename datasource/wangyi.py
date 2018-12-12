from datasource.utils import *
import requests
from datetime import date


def getDayData(code: str, end_date: date, start_date: date=date(1990, 1, 1)):
    url = ("http://quotes.money.163.com/service/chddata.html?"
           "code={0}&start={1}&end={2}&fields="
           "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(
        addWangyiPrefix(code), start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')))
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'gbk'
    return response.text


def getAllCloseData(code,period='day', fq=True):
    if not fq:
        kline = 'kline'
    else:
        kline = 'klinederc'
    url = 'http://img1.money.126.net/data/hs/%s/%s/times/%s.json' % (kline, period,addWangyiPrefix(code))
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def getYearlyDaysData(code,year,period='day'):
    url = 'http://img1.money.126.net/data/hs/kline/%s/history/%s/%s.json' % (period, year, addWangyiPrefix(code))
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def getTodayCurve(code):
    url = 'http://img1.money.126.net/data/hs/time/today/%s.json' % addWangyiPrefix(code)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get4DaysCurve(code,timeout=5):
    url = 'http://img1.money.126.net/data/hs/time/4days/%s.json' % addWangyiPrefix(code)
    response = requests.get(url,timeout=timeout)
    response.raise_for_status()
    return response.json()
