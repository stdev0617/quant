import pandas as pd
import numpy as np
import FinanceDataReader as fdr

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/naver_finance/2015_12.csv")
df = df.rename(columns={"ticker": "종목명"})


# (중요) 연산 기준
# DataFrame은 기준이 columns
# Series는 기준이 index
# 따로 명시가 없다면 Series는 index, DataFrame은 columns에 대해서 "먼저 align을 하고" 연산이 일어납니다.
# (참고) 앞에서는 스칼라 값 하나가 broadcasting이 되어 Series와 같은 형태를 만들어서 연산이 되었고,
# 여기서는 Series가 broadcasting 되어 DataFrame과 같은 형태를 만들어서 연산이 진행됩니다.
# 이 broadcasting은 Pandas 내부적으로 일어나서 연산이 진행됩니다.
def basic_arithmetic():
    price_df = fdr.DataReader("005930",'2009-09-16','2018-03-21')
    print(price_df.head())

    # Subtract row Series
    print((price_df - price_df.iloc[0]).head())

    # Subtract Column Series [X] (price_df['open'] - price_df도 마찬가지로 [X] )
    # dataframe의 결과가 다 nan으로 나옴
    (price_df - price_df['Open']).head(2)

    # DataFrame & DataFrame
    # index, column이 일치하는 것 끼리만 element-wise 연산이 이루어지고 나머지는 nan 처리
    (price_df - price_df[['Open', 'Low']].iloc[:2])

# 연산 관련 built-in 함수 사용
# axis란?
# 연산은 기본적으로 "axis를 변형(줄이거나 늘리는)하는 방식"
### numpy로 맛보기
def axis():

    a = np.array([1,2,3])
    b = np.array([1,2,3])

    print(np.sum([a, b], axis=0)) # y축 끼리 더함. a와 b 각각의 인덱스 위치의 값들을 더함. 결과는 [2 4 6]
    print(np.sum([a, b], axis=1)) # x축 끼리 더함. a의 모든 값을 더해서 하나의 값을, b의 모든 값을 더해서 하나의 값을 떨굼.
