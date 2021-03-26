import pandas as pd
import numpy as np
import FinanceDataReader as fdr

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

df = pd.read_csv("D:/inflearn_pandas_part1_material/my_data/naver_finance/2016_12.csv")
#df = df.rename(columns={"ticker": "종목명"})

# 엑셀시트에 price2라고 된 컬럼은 2017년의 가격임
def calculateEarningRate():
    df['rtn'] = df['price2'] / df['price'] - 1

    # Give group-number(or score) according to PER
    # Different number of members in each group
    # boolean indexing & loc 사용
    # 뒤에 Grouping by continuous variable section에서는 더 쉽게 가능
    board1 = df['PER(배)'] >= 10
    board2 = (5 <= df['PER(배)']) & (df['PER(배)'] < 10)
    board3 = (0 <= df['PER(배)']) & (df['PER(배)'] < 5)
    board4 = df['PER(배)'] < 0

    df.loc[bound1, 'PBR(배)'] = 1 # bound1의 조건을 만족하는 row에 대해서 PBR 값을 1로 덮어씌움.

    df.loc[board1] # get operation. 즉, 어떤 조건식이나 인덱스를 명시해서 원본데이터에서 추출
    df.loc[board1, 'PER_Score'] = 1 # set operation. 원본데이터의 특정 조건을 만족하는 어떤 컬럼이나 element에 대해서 원하는 값을 채워넣을 수 있음
                                    # dataframe이 가지고 있지 않은 컬럼이 들어오면? 해당 컬럼에 값을 채워주고, 나머지는 nan으로 처리한다.
    df.loc[board2, 'PER_Score'] = 2
    df.loc[board3, 'PER_Score'] = 3
    df.loc[board4, 'PER_Score'] = -1

    df['PER_Score'].head()
    df['PER_Score'].unique()

    # 데이터 분석을하는데 for loop을 돈다? 정말 다시 고민해보자 ㅎㅎ
    # 위의 방법들이 더 효과적이다.

    