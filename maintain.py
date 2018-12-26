# -*- coding: utf-8 -*-
from datasource import Maintainer
import timeit

ma = Maintainer()
#ma.downloadIndexes()

def f():
    ma.complementAllMT()
    
print(timeit.timeit('f()','from __main__ import f',number=1))
