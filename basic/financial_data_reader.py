import numpy as np
import pandas as pd
import FinanceDataReader as fdr

def useFinanceDataReader():
    # 삼성전자
    df1 = fdr.DataReader("005930", '2021-01-02', '2021-03-12')

    # KODEX 200 (ETF)
    df2 = fdr.DataReader("069500", '2021-01-02', '2021-03-12')

    print(df1.head())
    print()
    print(df2.tail())

    # row 하나 삭제
    df2 = df2.drop(pd.to_datetime("2021-03-12"))
    print(df2.tail())

    new_df2 = df2.reindex(df1.index)
    print(new_df2.tail())

    print(new_df2.fillna(method="ffill")) # nan이 나오면 이전 값으로 매꿈