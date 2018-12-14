import pandas as pd


def ADL(szzs,dfs,_date):
    ADL = []
    _index = szzs[_date:].index
    for dt in _index:
        sum_sz = 0
        sum_xd = 0
        for df in dfs:
            if dt in df.index:
                zde = df['涨跌额'][dt]
                if zde > 0:
                    sum_sz += 1
                elif zde < 0:
                    sum_xd +=1
        ADL.append(sum_sz-sum_xd)
    return pd.DataFrame(ADL,index=_index).cumsum()