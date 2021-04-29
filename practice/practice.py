import numpy as np
import pandas as pd

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('max_columns', None)

# Load data
# 데이터 출처: 증권사 API, N사 금융, 금투협, 유료 데이터 벤더
# Section2: 파일 읽는 법, EDA
def loadData():
    # 코드를 돌릴 때 warning이 안나오게 하기
    import warnings
    warnings.filterwarnings('ignore')

    # 영상에서는 fin_statement_2005_2017.csv이지만(데이터 문제가 있는 파일),
    # 해당 데이터에서 문제를 발견하여, fin_statement_new.csv라는 데이터(2006 ~ )로 대체되었습니다
    df = pd.read_csv("my_data/fin_statement_new.csv")
    df.head()

    # "12개월전대비수익률(현금배당포함)" 컬럼은 미리 제거하여 파일을 업로드했습니다
    df = df.drop(["상장일"], axis=1)

    df = df.rename(columns={
        "DPS(보통주, 현금+주식, 연간)": "DPS",
        "P/E(Adj., FY End)": "PER",
        "P/B(Adj., FY End)": "PBR",
        "P/S(Adj., FY End)": "PSR",
    })

    # 새로 올린 데이터는 2005가 아닌 2006부터 데이터가 존재합니다.
    df.groupby(['year'])['Name'].count()
    df.groupby(['Name'])['year'].count()

    # 회사 code, 이름 등이 같을 수 있음(합병 등의 이유로)
    # code or name의 중복 체킹 방법1
    df.groupby(['year'])['Name'].nunique().equals(df.groupby(['year'])['Code'].nunique())

    # code or name의 중복 체킹 방법2
    df.groupby(['year', 'Name'])['Code'].nunique()

    df.groupby(['year', 'Name'])['Code'].nunique().nunique()

def getYearlyReturns():
    df[df['Name'] == '동화약품']
    # section 4 "pivot" 참고 (pivot은 df를 변형시킴)
    yearly_price_df = df.pivot(index="year", columns="Name", values="수정주가")
    yearly_price_df.head()

    # rtn 구하기
    # 𝑝𝑛+1𝑝𝑛  - 1
    # 1. year_price_df.pct_change() == year_price_df / year_price_df.shift() - 1
    # 2. `shift(-1)`을 하는 이유?
    #    - 데이터를 "xx년도에서 1년동안 들고있었더니, xx만큼 수익이 났다"로 해석하고 싶기 때문
    yearly_rtn_df = yearly_price_df.pct_change(fill_method=None).shift(-1)
    yearly_rtn_df.head()

    # look ahead bias(미래를 미리 볼 수 있을 때 발생할 수 있는 편향)는 반드시 주의해야하는 부분
    # 자칫하면 백테스팅을 할 때, 미래의 정보를 보고 시뮬레이션을 하는 결과를 낳을 수 있음

    # 상장폐지 종목은 어떻게 처리가 되나?
    yearly_price_df['AD모터스']
    yearly_price_df['AD모터스'].pct_change(fill_method=None).shift(-1)

    # 2011/12에 매수했으면, 1년의 rtn value는은 보장됨.
    # 2012/12에 매수했으면,
    # 2013년 1월에 상장폐지 되었을 수도 있고, 2013년 12월(초)에 되었을 수도 있기 때문에 => rtn이 nan처리됨

