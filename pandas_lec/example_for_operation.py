import pandas as pd
import numpy as np
import FinanceDataReader as fdr

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

def exampleForOperation():
    b = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/multi_price.csv", index_col=[0])
    print(b.head())

    # 모멘텀 구하기
    momentum_series = b.loc["2018-08-09"] / b.loc["2017-08-09"] - 1 # 1년전과 비교해서 얼마나 증가했나?
    print(momentum_series.nlargest(3)) # 가장 많이 증가한거 3개 가져오기

