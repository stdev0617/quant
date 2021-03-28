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

    df.loc[board1, 'PBR(배)'] = 1 # bound1의 조건을 만족하는 row에 대해서 PBR 값을 1로 덮어씌움.

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

    # PER_Score 컬럼이 float으로 나오는 이유?
    # nan이 있으면, float으로 처리되기 때문에, 컬럼의 값들이 integer라도, nan이 껴있으면 float으로 처리됨

    df['PER_Score'].hasnans
    df['PER_Score'].isna().sum() # 왜 값이 12개가 나올까? 애초에 원본 데이터인 PER의 값에 nan이 껴있었기 때문!
                                 # 데이터를 분석할 때, 항상 먼저 nan을 검사하고, 처리하는 습관을 들이자.!
    df['PER(배)']
    df[df['PER(배)'].isna()] # 다른 값들은 있는데 왜 PER은 nan일까? 크롤링을 하면서 잘못된 데이터를 가져왔을수도 있고, 실제로 데이터가 없을수도 있고..
                             # 이런경우에는 다음이나 증권사로부터 데이터를 가져와서 메ㅜ꺼야한다
    df.loc[df['PER_Score'].isna(), "PER_Score"] = 0
    df['PER_Score'] = df['PER_Score'].fillna(0)
    df.loc[:, 'PER_Score'] = df['PER_Score'].fillna(0) # :의 의미는 '모든 컬럼'을 의미함. pandas에서는 이 방법을 추천함

    # Boolean series 연산 특성을 이용해서 PER 그룹 나누기
    df.loc[:, "PER_Score1"] = (board1 * 1) + (board2 * 2) + (board3 * 3) + (board4 * -1)
    df['PER_Score1'].value_counts()
    df['PER_Score'].value_counts() # 위는 int 이거는 float

    # 위의 두 score series는 서로 같을까?
    df['PER_Score'].equals(df['PER_Score1']) # equls로 nan 데이터에 대한 비교도 가능하게 했지만.. 결과는 false
    df['PER_Score'].dtypes
    df['PER_Score1'].dtypes
    df['PER_Score'].astype(int).equals(df['PER_Score1']) # 이런걸 unit test정도로 등록해두면 좋다

    # cut 실습
    per_cuts = pd.cut(
        df['PER(배)'],
        [-np.inf, 0, 5, 10, np.inf],
    )
    print(per_cuts) # -inf ~ 0 이 하나의 그룹, 0~5가 하나의 그룹, 5~10, 10~inf까지가 하나의 그룹으로 묶인다
    print(per_cuts.value_count()) # 그룹의 갯수가 출력됨

    bins = [-np.inf, 10, 20, np.inf]
    labels = ['저평가주','보통주','고평가주']
    per_cuts2 = pd.cut(
        df['PER(배)'], bins=bins, labels=labels
    )
    print(per_cuts2.head())
    df.loc[:, 'PER_Score2'] = per_cuts # per_cuts2