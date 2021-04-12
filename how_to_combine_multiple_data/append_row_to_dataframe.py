import matplotlib
import pandas as pd
import numpy as np
import FinanceDataReader as fdr

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/naver_finance/2016_12.csv")

# Append without using append() (using loc)
def appendWithoutUsingAppend():
    df = pd.DataFrame(columns=['a', 'b'])
    df.head()

    df.loc[["인덱스이름"]]
    df.loc[cond,"컬럼명"]

    # Add data as "list"
    df.loc[0] = [1,  2] # loc이 등호(=, assign)와 같이 나타난다면, set operation 진행
    df.loc['ㅋㅋ'] = [1, 2]
    df.head()

    df.loc[len(df)] = {'a': 'ㅋ', 'b': 'ㅎ'}
    df.head()

    df.loc["yay"] = pd.Series({'a': 'ㅋ', 'b': 'ㅎ'})
    df.tail()

    # 이미 존재하는 index에 넣기
    df.loc["yay"] = pd.Series({'a': '1111', 'b': '2222'})
    df.tail()

    # 위 방법들은 다 inplace 방식임
    # inplace란 특정 df가 있을 때, 메모리에 올려진 원본데이터의 값을 변형시키는 것을 의미함
    # inplace가 아닌 방식은 원본데이터를 복사하고, 그 복사된 메모리 위치에서 내용을 변형시키는 것을 의미함
    # 즉, inplace는 copy가 이루어지지 않기 때문에 속도상에 이점이 있음

# 위의 loc과는 다르게 not-in-place(returns a new copy of the DataFrame)
# append(): it only accept
#   - DataFrame
#   - Series
#   - Dictionary
#   - list of these(Not list itself)
def appendUsingAppend():
    names_df = pd.DataFrame(
        {
            'Name': ['철수', '영희', '영수', '영미'],
            'Age': [12, 13, 14, 15]
        },
        index = ['Canada', 'Canada', 'USA', 'USA']
    )
    print(names_df)

    #Error(에러내용 확인!) => index를 뭐로 실행해야할지 모르기 때문
    names_df.append(
        {'Name': '명수', 'Age': 1}
    )

    # ignore_index=True
    # 이전 index를 다 reset 한다.
    names_df.append(
        {'Name': '명수', 'Age': 1},
        ignore_index=True
    )

    # 리스트로도 전달 가능
    names_df.append(
        [
            {'Name': '명수', 'Age': 1},
            {'Name': '동수', 'Age': 2}
        ],
        ignore_index=True
    )

    names_df

    # Old index 유지하기 => append() 할 때, dict 대신에 Series를 전달하면 됨
    #   - Series를 append 할 때는, Series의 index가 column이 되고, name이 index가 됨.
    s = pd.Series({'Name': 'Zach', 'Age': 3}, name=len(names_df))
    print(s)

    print(names_df.append(s)) # 복제된 값을 리턴하기 때문에 결과가 출력됨

    # 리스트로도 전달 가능
    s1 = pd.Series({'Name': 'Zach', 'Age': 3}, name=len(names_df)) # name의 index가 row 갯수에 따라 순차적으로 늘어남
    s2 = pd.Series({'Name': 'Zayd', 'Age': 2}, name='USA')
    print(names_df.append([s1, s2]))

    # 참고: Series의 name은 어떤 operation을 하느냐에 따라서, index or column이 될 수 있음
    print(pd.concat([s1, s2], axis=1))

# DataFrame or Series object를 vertically or horizontally '연결'
# index(or columns)에 대해 align(not values)
# Defaults to outer join
#  - operation axis에 따라 concat되는 object의 column or index가 union 됨.
def using_concat():
    # 예제 1
    samsung_df = fdr.DataReader('005390', '2009-01-01', '2017-12-31')
    kodex_df = fdr.DataReader('069500', '2009-01-01', '2017-12-31')

    print(samsung_df.head(2))
    print(kodex_df.head(2))

    print(pd.concat([samsung_df, kodex_df]).head(2))

    # column, index alignment 특징은 그대로 적용됨!
    print(pd.concat([samsung_df, kodex_df[['Open', 'High']]]).head(2))
    print(pd.concat([samsung_df, kodex_df[['Open', 'High']]]).tail(2))

    # keys, names args
    # keys를 선언하면, 각 row가 어떤 key에 해당되는지 왼쪽에 컬럼이 추가되고
    # names를 선언하면, 그 keys와 index의 상위 attribute에 해당 속성이 추가된다.
    print(pd.concat([samsung_df, kodex_df], keys=['삼성', 'KODEX200'], names=['종목명']).head(2))
    print(pd.concat([samsung_df, kodex_df], keys=['삼성', 'KODEX200'], names=['종목명']).tail(2))

    print(pd.concat([samsung_df, kodex_df], keys=['삼성', 'KODEX200'], names=['종목명', '날짜']).head(2))

    # On axis=1
    print(pd.concat([samsung_df, kodex_df], axis=1).head())
    print(pd.concat([samsung_df, kodex_df], keys=['삼성', 'KODEX200'], axis=1).head(2))

    # join argument
    # - How to handle indexs on other axis(es), 즉, concat의 대상이 되는(=명시되는) axis 말고,
    # 다른 axis의 index에 대해 어떻게 join 할 것인가?
    # inner는 교집합, outer는 합집합이라고 생각하면됨
    result = pd.concat([df1, df4], axis=1, join='inner')
    
    # default 'outer' join
    pd.concat([samsung_df, kodex_df], keys=['삼성', 'kodex'], axis=1, names=['종목명']).head()
    
    # join = inner (date intersection)
    pd.concat([samsung_df, kodex_df], keys=['삼성', 'kodex'], axis=1, names=['종목명'], join='inner').head()

    # concat 방향이 axis=0 이니까, axis=1에 대해서 join이 적용됨
    pd.concat([samsung_df.head(), kodex_df[['Close']].head()], join='inner')

    # 주의: column명이 다를 때! => alignment가 일치하는게 없으니 NaN으로 메꾼다!
    samsung_diff_col_df = samsung_df.copy()
    samsung_diff_col_df.columns = ['1_'+col for col in samsung_df.columns]
    print(samsung_diff_col_df.head())

    print(pd.concat([samsung_diff_col_df, kodex_df]).head())

# concat을 이용해서 close 데이터만 뽑아내기
def concatExample():
    total_df = pd.concat([samsung_df, kodex_df], keys=['삼성', 'kodex200'], names=['종목명'])
    print(total_df.head())
    print(total_df.tail())

    total_df = total_df.reset_index()
    total_df.head()

    total_df.pivot('Date', '종목명', 'Close').tail()

    # pivot
    sample_data = pd.DataFrame(
        {
            "종목명": ["삼성", "현대", "하이닉스", "삼성", "현대", "하이닉스"],
            "datetime": ["2019-01-01", "2019-01-01", "2019-01-01", "2019-01-02", "2019-01-02", "2019-01-02"],
            "price": [1, 2, 3, 4, 5, 6]
        }
    )

    print(sample_data)

    sample_data.sort_values("종목명")

    # date별로, 각 종목의 close 값을 다 가져옴
    sample_data.pivot(index="datetime", columns="종목명", values="price")

    # join()
    # Used when 2 potentially differently differently-indexed Dataframes into a single result DataFrame
    # Aligns the calling DataFrame's 'column(s) or 'index' with the other objects 'index'
    #   - index- index
    #   - columns - index (calling object는 column, arg object는 index)
    #      - 'on' arg = calling object의 column
    #        - called object의 index를 calling object의 '어떤 column'에 맞출것인가
    #      - set_index() 후, 'on'없이 index-index join과 같은 결과
    #   - concat과 달리, index, column명이 아니라, value 값 자체를 이용한 join
    #   - cartesian product joining
    #   - Defaults to left join
    # 결론: join()은 특정 컬럼의 값이 같은 것을 기준으로 두 데이터프레임을 하나로 합친다.
    #      concat()은 index나 column 이름을 기준으로 두 데이터 프레임이 하나로 합쳐진다.

    left = pd.DataFrame({'A': ['A0', 'A1', 'A2'], 'B': ['B0', 'B1', 'B2']}, index=['K0', 'K1', 'K2'])
    right = pd.DataFrame({'C': ['C0', 'C2', 'C3'], 'D': ['D0', 'D2', 'D3']}, index=['K0', 'K2', 'K3'])

    print(left)
    print(right)

    left.join(right) # left의 교집합. left를 기준으로 K1 index의 C, D 값이 NaN이고 나머지는 쭉 붙음.
    left.join(right, how='outer')  # 합집합. 단, 값이 없는것은 NaN으로 뜸.

    left = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'], 'B': ['B0', 'B1', 'B2','B3']}, index=['K0', 'K1', 'K0', 'K1'])
    right = pd.DataFrame({'C': ['C0', 'C1'], 'D': ['D0', 'D1']}, index=['K0', 'K1'])

    print(left)
    print(right)

    # 아래 내용은 join()과 concat()의 큰 차이점 중 하나임.
    # 분명 left는 key column의 값에 K0, K1이 있지만, on='key를 통해서 right의 index가 key 컬럼의 값에 기준을 맞춰서 하나가 됨.
    left.join(right, on='key')
    left.join(right, on='key').set_index("key")
    left.set_index('key').join(right)
