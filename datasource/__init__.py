import requests
from datasource import utils
import xlrd
import os
from bs4 import BeautifulSoup
from datetime import date,datetime,timedelta
import pandas as pd
import numpy as np


class SHExchange:
    def __init__(self):
        self.__header = {
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
        }
        self.__base_url = "http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=%d"

    def __get(self, url):
        res = requests.get(url, headers=self.__header)
        res.raise_for_status()
        return res.text

    def getCurrentCodes(self):
        text = self.__get(self.__base_url.replace('%d', '1'))
        h = utils.CSVHelper(text)
        next(h)
        return [row[0:6] for row in h]

    def getDelisted(self):
        text = self.__get(self.__base_url.replace('%d', '5'))
        h = utils.CSVHelper(text)
        next(h)
        return [row[0:6] for row in h if not row.startswith('900')]
    
    def getHalted(self):
        text = self.__get(self.__base_url.replace('%d', '4'))
        h = utils.CSVHelper(text)
        next(h)
        return [row[0:6] for row in h if not row.startswith('900')]
    
    def getAllCodes(self):
        return self.getCurrentCodes()+self.getDelisted()+self.getHalted()


class SZExchange:
    def __init__(self):
        self.__base_url = 'http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=%s&TABKEY=tab%d'
        
    def __get(self,url,col=0):
        res = requests.get(url)
        res.raise_for_status()
        with open('tmp.xlsx', 'wb') as f:
            f.write(res.content)
            f.close()
        wb = xlrd.open_workbook('tmp.xlsx')
        sheet = wb.sheet_by_index(0)
        ret = []
        for i in range(1, sheet.nrows):
            code = sheet.row(i)[col].value
            if not code.startswith('200'):
                ret.append(code)
        os.remove('tmp.xlsx')
        return ret
    
    def getCurrentCodes(self):
        url = self.__base_url % ('1110',1)
        return self.__get(url)
    
    def getDelisted(self):
        url = self.__base_url % ('1793_ssgs',2)
        return self.__get(url)
    
    def getHalted(self):
        url = self.__base_url % ('1793_ssgs',1)
        return self.__get(url)
    
    def getAllCodes(self):
        return self.getCurrentCodes()+self.getDelisted()+self.getHalted()


class Wangyi:
    def getDayData(self, code, end_date, start_date='19900101'):        
        url =  "http://quotes.money.163.com/service/chddata.html?code={0}&start={1}&end={2}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(
                utils.addWangyiPrefix(code),
                start_date, 
                end_date)
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'gbk'
        return response.text


    def getIndexData(self,code, end_date):
        url = "http://quotes.money.163.com/service/chddata.html? \
              code=%s&start=19900101&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER" % (code,end_date)
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'gbk'
        return response.text


    def peekDayData(self,code, _date):
        url = "http://quotes.money.163.com/trade/lsjysj_%s.html#01b07" % code
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.findAll('table')[3]
        ret = []
        for tr in table.findAll('tr'):
            data = [td.text for td in tr.findAll('td')]
            if not data:
                continue
            if data[0] <= _date:
                return ret
            else:
                data[7] = data[7].replace(',', '')
                data[8] = data[8].replace(',', '')
                ret.append(data)
        return ret


class Maintainer:
    def __init__(self):
        self.__sh_exchange = SHExchange()
        self.__sz_exchange = SZExchange()
        self.__wy = Wangyi()
        self.__stocks_folder = 'E:/quant/data/stocks/'
        self.__indexes_folder = 'E:/quant/data/indexes/'
    
    @property
    def stocks_folder(self):
        return self.__stocks_folder
    
    @property
    def indexes_folder(self):
        return self.__indexes_folder
    
    def downloadSingle(self,code,end_date:date=date.today().strftime('%Y%m%d')):
        content = self.__wy.getDayData(code, end_date)
        helper = utils.CSVHelper(content)
        next(helper)
        latest_date = next(helper)[0:10]
        with open(self.__stocks_folder + latest_date + '-' + '%s.csv' % code, 'w', newline='') as f:
            f.write(content[0:62])
            helper = utils.WYRCSVHelper(content,62)
            f.writelines(helper)
            
    def complementDownloadAll(self):
        downloaded = [name[11:17] for name in os.listdir(self.__stocks_folder)]
        sh_codes,sz_codes = self.__sh_exchange.getAllCodes(), self.__sz_exchange.getAllCodes()
        _date = date.today().strftime('%Y%m%d')
        for codes in sh_codes,sz_codes:
            for code in codes:
                if code in downloaded:
                    continue
                self.downloadSingle(code,_date)
          
    def reDownloadAll(self):
        sh_codes,sz_codes = self.__sh_exchange.getAllCodes(), self.__sz_exchange.getAllCodes()
        end_date = date.today().strftime('%Y%m%d')
        for codes in sh_codes,sz_codes:
            for code in codes:
                content = self.__wy.getDayData(code, end_date)
                helper = utils.CSVHelper(content)
                next(helper)
                latest_date = next(helper)[0:10]
                with open(self.__stocks_folder + latest_date + '-' + '%s.csv' % code, 'w', newline='') as f:
                    f.write(content[0:62])
                    helper = utils.WYRCSVHelper(content,62)
                    f.writelines(helper)
    
    def complementAll(self):
        end_date = date.today()
        for name in os.listdir(self.__stocks_folder):
            last_date = datetime.strptime(name[0:10], '%Y-%m-%d').date()
            if end_date > last_date:
                code = name[11:17]    
                start_date = last_date+timedelta(1)
                content = self.__wy.getDayData(code, end_date.strftime('%Y%m%d'), start_date.strftime('%Y%m%d'))
                helper = utils.CSVHelper(content)
                next(helper)
                try:
                    latest_date = next(helper)[0:10]
                    path = self.__stocks_folder + name
                    with open(path, 'a') as f:
                        f.writelines(utils.WYRCSVHelper(content,62))
                    os.rename(path, self.__stocks_folder + latest_date + '-' + '%s.csv' % code)
                except StopIteration:
                    continue
                
    def downloadIndexes(self):
        indexes = ['0000001','0000016','0000300',
                   '1399001','1399106','1399006','1399102']
        dt = datetime.now()
        _date = dt.date()
        if dt <  datetime(_date.year, _date.month, _date.day,15,30,0):
            _date -= timedelta(1)
        for index in indexes:
            content = self.__wy.getIndexData(index, _date.strftime('%Y%m%d'))
            with open(self.__indexes_folder+ '%s.csv' % index[1:], 'w', newline='') as f:
                f.write(content[0:48])
                helper = utils.WYRCSVHelper(content,48)
                f.writelines(helper)
                
    def getDateUnmatched(self):
        ret = []
        for name in os.listdir(self.__stocks_folder):
            lastest_date = datetime.strptime(name[0:10],'%Y-%m-%d')
            with open(self.__stocks_folder + name, 'r') as f:
                content = f.readlines()
                target_date = datetime.strptime(content[-1][0:10],'%Y-%m-%d')
                if  target_date!= lastest_date:
                    ret.append(name)
        return ret
    
    def readAllStocks(self):
        return [pd.read_csv(self.__stocks_folder + name, encoding='gbk', index_col=0,
                        converters={
                                '收盘价':utils.NoneZeroFloat,
                                '最高价':utils.NoneZeroFloat,
                                '最低价':utils.NoneZeroFloat,
                                '开盘价':utils.NoneZeroFloat,
                                '前收盘':utils.NoneZeroFloat,
                                '涨跌额':utils.Float,
                                '涨跌幅':utils.Float,
                                '换手率':utils.NoneZeroFloat,
                                '成交量':utils.NoneZeroInt,
                                '成交金额':utils.NoneZeroFloat,
                                '总市值':utils.NoneZeroFloat,
                                '流通市值':utils.NoneZeroFloat
                                }) for name in os.listdir(self.__stocks_folder)]

    
    def readStock(self,code):
        names = [name for name in os.listdir(self.__stocks_folder)]
        for name in names:
            if code in name:
                return pd.read_csv(self.__stocks_folder+name,encoding='gbk',index_col=0,
                        converters={
                                '收盘价':utils.NoneZeroFloat,
                                '最高价':utils.NoneZeroFloat,
                                '最低价':utils.NoneZeroFloat,
                                '开盘价':utils.NoneZeroFloat,
                                '前收盘':utils.NoneZeroFloat,
                                '涨跌额':utils.Float,
                                '涨跌幅':utils.Float,
                                '换手率':utils.NoneZeroFloat,
                                '成交量':utils.NoneZeroInt,
                                '成交金额':utils.NoneZeroFloat,
                                '总市值':utils.NoneZeroFloat,
                                '流通市值':utils.NoneZeroFloat
                                })
    
    
    def readIndex(self,code):
        return pd.read_csv(self.__indexes_folder+code+'.csv',encoding='gbk',index_col=0,
                       converters={
                                '收盘价':utils.NoneZeroFloat,
                                '最高价':utils.NoneZeroFloat,
                                '最低价':utils.NoneZeroFloat,
                                '开盘价':utils.NoneZeroFloat,
                                '前收盘':utils.NoneZeroFloat,
                                '涨跌额':utils.Float,
                                '涨跌幅':utils.Float,
                                '成交量':utils.NoneZeroInt,
                                '成交金额':utils.NoneZeroFloat
                               })
            
    def complementOnline(self,df):
        r = df.iloc[len(df)-1]
        code = r['股票代码']
        shares1 = r['总市值'] / r['收盘价']
        shares2 = r['流通市值'] / r['收盘价']
        datas = self.__wy.peekDayData(code[1:],r.name)
        for data in reversed(datas):
            row = {'股票代码':code,'名称':r['名称'],'收盘价':np.float(data[4]),
                   '最高价':np.float(data[2]),'开盘价':np.float(data[1]),'最低价':np.float(data[3]),'涨跌额':np.float(data[5]),
                   '涨跌幅':np.float(data[6]),'成交量':int(data[7])*100,'成交金额':np.float(data[8])*10000,'换手率':np.float(data[10]),
                   '前收盘':r['收盘价'],'总市值':shares1*np.float(data[4]),'流通市值':shares2*np.float(data[4])}
            df.loc[data[0]] = row

if __name__=='__main__':
    ma = Maintainer()
    r = ma.readStock('300183')
    ma.complementOnline(r)