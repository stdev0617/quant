import pandas as pd
import numpy as np
import FinanceDataReader as fdr

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/naver_finance/2015_12.csv")
df = df.rename(columns={"ticker": "종목명"})

def dealWithNanValue():
    print(None==None)
    print(np.nan == np.nan)
    print(5<np.nan)
    print(5>=np.nan)
    # 아래 operation만 true.
    print(np.nan!=5)
    df1 = pd.DataFrame(
        {
            'a':[1,2,3],
            'b':[np.nan, 4, np.nan],
        }
    )
    print(df1)
    print(df1['b'] == df1['b']) # nan값을 갖는건 모두 false, 숫자4는 true

    print(df1.ge(2)) # Same with (df1 >= 2)
    print(df1.le(2))

    print(df.head())
    print(df['PER(배)'] > 1)
    print(df['PER(배)'].count())

    print(df['PER(배)']==np.nan) # false
    print((df['PER(배)']==np.nan).any()) # false

    # Nan Checking
    # For Series
    print(df['순이익률(%)'].hasnans) # true / false

    # Generate boolean series
    print(df['순이익률(%)'].isna())
    print(df['순이익률(%)'].isnull()) # isna와 같음. 함수명만 다름
    print(df['순이익률(%)'].isnull().sum())
    print(df['순이익률(%)'].isnull().any())

    print(df.isnull().head())
    print(df.isnull().any()) # default axis=0. 각 column값마다 null이 있는지 확인
    print(df.isnull().any().any()) # dataframe에 nan값이 하나라도 있는지 확인
    print(df.isnull().any().all()) # isnull().any()의 결과가 하나라도 nan이 있는지 확인

    print(df1['b'] == df1['b']) # 시리즈간에 비교하면 엘리먼트 와이즈밖에 안됨
    print(df1['b'].equals(df1['b'])) # dataframe 또는 series자체가 완전히 똑같냐? 데이터 타입도 체킹함

def checkNanExample():
    _df = pd.DataFrame({'a':[1,np.nan,3], 'b':[np.nan, 2, 3]})
    print(_df.head())

    # nan이 하나라도 들어있으면 날려버리고 싶은 경우
    # 둘 다 nan이 아닌 값들만 추출
    print(_df['a'].notnull())
    print(_df['b'].notnull())
    print(_df[_df['a'].notnull() & _df['b'].notnull()])

    print(_df[_df.notnull().all(axis=1)])
    print(_df.dropna())

    # subset에 있는 컬럼 중에 하나라도(혹은 전부, arg로 선택가능) null이면 drop한다.
    print(_df.dropna(subset=['a']))