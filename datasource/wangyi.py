from datasource.utils import *
import requests
from datetime import date
from bs4 import BeautifulSoup


def getDayData(code: str, end_date: date, start_date: date=date(1990, 1, 1)):
    url = ("http://quotes.money.163.com/service/chddata.html?"
           "code={0}&start={1}&end={2}&fields="
           "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(
        addWangyiPrefix(code), start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')))
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'gbk'
    return response.text


def getIndexData(code, end_date):
    url = "http://quotes.money.163.com/service/chddata.html?" \
          "code=%s&start=19900101&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER" % (code,end_date.strftime('%Y%m%d'))
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'gbk'
    return response.text


def peekDayData(code: str, _date: date):
    url = "http://quotes.money.163.com/trade/lsjysj_%s.html#01b07" % code
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.findAll('table')[3]
    s_date = _date.strftime('%Y-%m-%d')
    ret = []
    for tr in table.findAll('tr'):
        data = [td.text for td in tr.findAll('td')]
        if not data:
            continue
        if data[0] < s_date:
            return ret
        else:
            data[7] = data[7].replace(',', '')
            data[8] = data[8].replace(',', '')
            ret.append(data)
    return ret
             
            
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
