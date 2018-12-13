import pandas as pd


def ZDGS(szzs, dfs):
    return pd.DataFrame({i:dfs[i]['涨跌额'] for i in range(0,len(dfs))})