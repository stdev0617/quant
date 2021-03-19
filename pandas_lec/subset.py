import pandas as pd
import numpy as np

# dataframe이 있을 때, 전체가 아니라 일부분을 가져와서 dataframe으로 저장하는 방법
# 1. column을 가지고 subset을 가져오는 방법
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/naver_finance/2015_12.csv")

def subsetByColumns():
    df.head()
    print(df['EPS(원)'])
    print(type(df['순이익률(%)'])) # series로 데이터가 나옴
    df2 = df[['EPS(원)', 'ticker']]
    print(df2) # dataframe으로 결과나 나옴.
    print(df[['순이익률(%)']]) # dataframe으로 결과가 나옴. 즉, df안에 리스트를 사용하면 결과는 dataframe. 안쓰면 series로 리턴
    print(type(df[['순이익률(%)', '당기순이익(억원)']]))
    print(df.filter(like="P").head()) # like 연산으로 해당 조건에 맞는 column의 dataframe을 가져온다
    print(df.filter(regex="P+\w+R").head()) # \w는 문자열이 1개 이상 있다는 뜻. +는 연결. 즉, P로 시작하고, R로 끝나는 문자를 찾음. 정규표현식을 공부하자

def useDtype():
    print(df.get_dtype_counts()) # datatype 갯수를 보여줌
    print(df.select_dtypes(include=['float']).head()) # 특정 타입의 데이터만 보여줌
    print(df.select_dtypes(include=['object']).head())

def useIlocAndLoc():
    name_df = df.set_index("종목명")
    print(name_df.head())
    print(name_df[0]) # 컬럼이 '0'인 series를 가져오라는 뜻
    print(name_df.iloc[0]) # 0번째 row의 데이터를 가져옴
    print(name_df.iloc[[0, 1]].head(1)) # i는 int로 indexing한다고 보면됨.
    print(name_df.loc[['삼성전자', 'CJ']]) # index 이름 자체를 가지고 row를 가져옴. 중요중요중요중요

    # 반드시 index를 sort 해야만 가능
    name_df = name_df.sort_index()
    print(name_df.head()) # 이걸로는 인덱스가 sort되었는지 알 수 없음
    print(name_df.index.is_monotonic_increasing) # true가 나오면 정렬이 잘 되어있다는 뜻임
    print(name_df.loc["삼성":"삼성전자"]) # 기본 리스트와는 다르게, 삼성~삼성전자까지 문자를 포함해서 조사한다. my_list[:3]은 0,1,2 출력
    print(name_df.loc["가":"다"].head(2))

    #string, list
    print(name_df.loc["삼성전자", "순이익률(%)"]) # 삼성전자의 순이익률을 가져올 수 있음. 즉, 첫번째 인자는 row값, 두번째 인자는 컬럼임.
    print(name_df.loc["삼성전자"]["순이익률(%)"]) # 이것도 가능하지만, 판다스에서는 위의 방식을 권장함.
    print(name_df.loc[["삼성SDI","삼성전자"],["순이익률(%)", "EPS(원)"]]) # 이렇게 하면 multi row, multi column 검색 가능

    print(name_df.iloc[[0,3], [0,1]]) # 이렇게 사용
    # name_df.iloc[[0,3], ["상장일","종가"]] 이건 error

    a = pd.Series([1,2,3], index=['a','b','c'])
    a['a']
    a.iloc[0] # scalar
    a.iloc[[2]] # series

    df.iloc[2] # scalar
    df.iloc[[2]] # series

def useAt():
    # dataframe의 특정 scalar 값을 가져오고싶을 때, 특정 row와 특정 column에 해당되는 값을 가져오고싶을 때.
    print(df.loc[100, '순이익률(%)'])
    print(df.at[100, '순이익률(%)']) # 순이익률 컬럼의 100번째 row 값
    ## Much faster if use '.iat' or '.at' than '.loc'
    # => Table이 크면 클 수록 더 차이가 많이 난다.
    # %timeit df.loc[100, '순이익률(%)'] # %time iteration. 주피터에서 실행시간을 측정해줌

def useBooleanSeries():
    tmp_series = pd.Series({"a":1, "b":2})
    print(tmp_series > 2) # 데이터가 series로 나오는데, nan과 비교시 무조건 false로 나옴.
    print(df['순이익률(%)'].head())
    print(df['영업이익률(%)'].head())

    a = df['순이익률(%)'] > df['영업이익률(%)']
    print(a.head()) # 비교한 결과 시리즈가 쭉 나옴
    print(a.sum()) # true인 것들의 합
    print(a.mean())
