import pandas as pd
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

#EDA란, 데이터를 추출해서 summarize를 하거나 visualizing을 통해 특징을 찾아내는 것
#즉, 데이터의 특성을 발견하는 것
# Two Parts
# 1. Metadata: data about data
# 2. Univariate descriptive statistics: summary statistics about individual variables(columns) -> 평균, 분포 등을 보는 것

def test_eda():
    # 1. EDA 기초
    df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/naver_finance/2015_12.csv")
    print(df.head())

    print(df.shape)
    print(df.dtypes.value_counts()) # dataType Counts. 예제는 float64가 14개 object가 1개가 있다고 나옴
                                    # 강의에서는 df.get_dtype_count()를 사용하였으나, 내가 쓰는 버전에서는 deprecated 됨
    print(df.info) # 모든 column의 정보를 보고 싶을때. df.info()가 아니라 df.info임
    print(df['ticker'].dtype) # series의 데이터 타입을 보고 싶은 경우

    df = df.rename(columns={"ticker": "종목명"}) # 특정 컬럼의 이름을 변경
    print(df.head())

    # 2. describe 사용하기
    # describe는 count, mean, std, min, 25%, 50%, 75%, max 를 알 수 있음
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    print(df.describe())
    print(df.describe().T) # transformation 함. 즉, row와 column의 속성을 바꿈.

    # 1) numerical
    print(df.describe(include=[np.number]).T) # = df.describe()
    print(df.describe(percentiles=[0.01,0.03,0.99]).T.head(2)) # 하위 1%, 하위 3%, 하위 99%를 추가로 볼 수 있음

    # 2) categorical
    #include는 object, categorical 데이터 만
    print(df.describe(include=[np.object, pd.Categorical]).T.head()) # 'top' "가장 많이 나오는 단어"를 의미함. unique는 중복되지 않는 것의 갯수임.
                                                                     # 현재는 top이 의미없음. 다 1번씩 나오기때문
    # number 빼고 나머지
    print(df.describe(exclude=[np.number]).T.head())
    print(df['PER(배)'].quantile(.2))             # 하위 20% 값
    print(df['PER(배)'].quantile([.1, .2, .3]))   # 하위 10, 20, 30% 값