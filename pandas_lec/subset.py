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

def useAt():
    # dataframe의 특정 scalar 값을 가져오고싶을 때, 특정 row와 특정 column에 해당되는 값을 가져오고싶을 때.
    print(df.loc[100, '순이익률(%)'])
    print(df.at[100, '순이익률(%)']) # 순이익률 컬럼의 100번째 row 값
    ## Much faster if use '.iat' or '.at' than '.loc'
    # => Table이 크면 클 수록 더 차이가 많이 난다.
    # %timeit df.loc[100, '순이익률(%)'] # %time iteration. 주피터에서 실행시간을 측정해줌

