import requests
from bs4 import BeautifulSoup

def getAllCodes():
    '''
    东财的代码没有剔除已退市的股票
    :return:
    '''
    url = "http://quote.eastmoney.com/stocklist.html"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,'html.parser')
    r = soup.find_all('a')
    sh = "http://quote.eastmoney.com/sh6"
    sz = "http://quote.eastmoney.com/sz0"
    cyb = "http://quote.eastmoney.com/sz3"
    ret = []
    for a in r:
        s = a.get('href')
        if s is not None:
            if sh in s or sz in s or cyb in s:
                ret.append(s[-11:-5])
    return ret
