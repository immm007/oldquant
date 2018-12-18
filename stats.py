# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import date,timedelta

class ADL:
    def __init__(self,ref,stocks,path='None'):
        self.__ref = ref
        self.__stocks = stocks
        self.__path = path
        self.__ret = {'a':[],'d':[],'diff':[]}
        self.__result = None
    
    def calculate(self):
        if not os.path.exists(self.__path):
            return self.calculateFromScratch()
     
    def calculateFromScratch(self):
        self.__ret['a'].clear()
        self.__ret['d'].clear()
        self.__ret['diff'].clear()
        for _date in self.__ref.index:
            sum_a = 0
            sum_d = 0
            for stock in self.__stocks:
                if _date not in stock.index:
                    continue
                else:
                    if stock['涨跌额'][_date] > 0:
                        sum_a += 1
                    elif stock['涨跌额'][_date] < 0:
                        sum_d +=1
            self.__ret['a'].append(sum_a)
            self.__ret['d'].append(sum_d)
            self.__ret['diff'].append(sum_a-sum_d)
        self.__result = pd.DataFrame(self.__ret,index=self.__ref.index)
        return self.__result
    
    def drawADL(self,_date=(date.today()-timedelta(365)).strftime('%Y-%m-%d')):
        diff = self.__result['diff'].cumsum()
        plt.subplot(2,1,1)
        plt.plot(self.__ref['收盘价'][_date:])
        plt.subplot(2,1,2)
        plt.plot(diff[_date:])
        plt.show()