from datasource.utils import *
import requests

def getRTQuotes(codes):
    codes = [addSinaPrefix(code) for code in codes]
    url = "http://hq.sinajs.cn/list=%s" % ','.join(codes)
    response = requests.get(url)
    response.raise_for_status()
    return response.text