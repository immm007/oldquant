# -*- coding: utf-8 -*-
from datasource import Maintainer

ma = Maintainer()

#sh_stocks = ma.readAllStocks(ma.sh_predicate)
#sz_stocks = ma.readAllStocks(ma.sz_predicate)
cyb_stocks = ma.readAllStocks(ma.cyb_predicate)

#szzs = ma.readIndex('000001')
#szcz = ma.readIndex('399001')
cybz = ma.readIndex('399006')

for stock in cyb_stocks:
    ma.complementOnline(stock)
