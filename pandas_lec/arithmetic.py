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

    print(df[['순이익률(%)', 'PER(배)']].sum()) # default axis = 0, 즉, 순이익률의 모든 합, per의 모든 합이 결과로 리턴됨.
    print(df[['순이익률(%)', 'PER(배)']].mean()) # default axis = 0

    # 1. numpy array인 경우
    # a = np.array([[1, 2], [3, 4]])
    # 아래는 서로 다른 결과
    # a.sum(axis=None) # axis 구분없이 모든 element sum
    # a.sum(axis=0) # axis=0 방향으로 sum

    # 2. pandas DataFrame인 경우
    # df = pd.DataFrame(a)
    # 아래 둘은 같은 결과
    # df.sum(axis=None) # axis=0 방향으로 sum
    # df.sum(axis=0) # axis=0 방향으로 sum

    price_df = fdr.DataReader("005930",'2009-09-16','2018-03-21')
    print((price_df - price_df.mean()).head()) # 모든 row별로 각 컬럼의 mean값을 빼줌

    # dataFrame과 series간에 연산을 할 때, index와 column이 align이 안맞아서 생겼던 문제들을 해결할 수 있는 방법
    # 아래 구문은 연산 불가능 했었음
    close_series = price_df['Close']
    print(price_df - close_series)
    # 하지만 DataFrame이 제공하는 함수를 이용하면 가능
    # sub()의 경우 description에 'For Series input, axis to match Series index on'라고 써있음
    # axis=0 or 1은 무조건 description (shift + tab) 먼저 보고 판단하고 그 후에 "axis는 해당 axis를 변형(줄이거나 늘리는 것)" 적용하기
    print(price_df.sub(close_series, axis=0).head()) # sub는 subtract임. 쓰는건, 해당 dataframe에서 매칭을 시킬 axis를 명시해주면됨.
