import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

    # Single Indicator(지표) backtesting
    #   Section1: reset_index()
    #   Section2: boolean selection, DataFrame arithmetic operation, dtype변환
    #   Section3: groupby() & aggregation
    #   Section4: join(), pivot()
    #   Section5: visualization

    # DataFrame(matrix) Multiplication 복습
    # 1. Vectorized backtesting
    #  - 과거데이터를 하나의 벡터화(by numpy, pandas)하여, 백테스팅을 벡터들간의 연산으로 진행하는 것.
    # 수백~수천개의 과거데이터를 한 번에 처리할 수 있기 때문에 빠르다는 장점이 있음
    #
    # 2. Event-based backtesting
    #  - 위의 방법처럼 과거데이터를 하나로 묶어서 벡터화를 하는 것이 아닌, 데이터가 실제 이용가능한 시점을 event화 하여, 실제 각각의 데이터를 event마다 받아서 백테스팅하는 방법.
    # Vectorized 방법보다는 느리지만, 실제 주식시장에서의 로직을 그대로 반영하기 때문에 최소한의 코드 수정으로 실전에 바로 투입할 수 있는 장점이 있음

    # dataframe끼리의 곱은, 컬럼이 같은것 끼리만 곱해지고, 컬럼이 없는 상태로 곱해지면 nan이 됨
    # 동일가중: 내가 선택한 종목들에 대해서 같은 금액만큼 투자를 하겠다는 것
    def multiplicationExample():
        a = pd.DataFrame([[1, 2], [3, np.nan, ], [5, 6]], columns=["a", "b"])
        b = pd.DataFrame([[1, 2], [3, 4, ], [5, 6]], columns=["a", "b"]) * 10
        print(a)
        print(b)
        print(a*b)

        a = pd.DataFrame([[1, 2], [3, np.nan, ], [5, 6]], columns=["a", "b"])
        b = pd.DataFrame([[1, 2, 3], [3, 4, 5], [5, 6, 7]], columns=["c", "b", "d"]) * 10
        print(a)
        print(b)
        print(a*b)

        return_df = pd.DataFrame(
            [
                [np.nan, np.nan, 2],
                [3, np.nan, 3],
                [5, 6, np.nan],
            ],
            columns=["삼성", "현대", "SK"]
        )
        asset_on_df = pd.DataFrame(
            [
                [0, 1],
                [0, 1],
                [1, 0],
            ],
            columns=["삼성", "SK"]
        )
        return_df
        asset_on_df

        print(return_df * asset_on_df)
        print((return_df * asset_on_df).mean(axis=1)) # mean()을 구할 때, nan은 제외하고 연산이 진행됨.

        # 해결책
        asset_on_df = asset_on_df.replace(0, np.nan)

        print(return_df * asset_on_df)

        # "동일가중" 방식의 투자인 경우, 포트폴리오 평균수익률 구하는 방법
        (return_df * asset_on_df).mean(axis=1)

    #top_n
    def top_n():
        df.head()
        indicator = "ROA"
        top_n = 10
        # multi column의 경우, reser_index()를 사용하면 컬럼명이 없는 놈은 결과에 컬럼명이 붙어서 나옴. 단, level_1 등으로 나옴.
        # ROA 데이터가 없는 등 이런경우에는 어떻게 처리할지 고민이 필요함.
        top_n_indicator_df = df.groupby(['year'])[indicator].nlargest(top_n).reset_index()
        top_n_indicator_df.head()
        top_n_indicator_df.tail()
        # 종목 indexing
        top_n_roa_df = df.loc[top_n_indicator_df['level_1']]
        top_n_roa_df.head()
        # pivot()을 사용하면, column과 index를 서로 바꿔서 보여줄 수 있음.
        indicator_df = top_n_roa_df.pivot(index="year", columns="Name", values="ROA")
        indicator_df.head()

    # 주의: nan 값을 가지고 있는 종목은 아예 고려대상에서 배제됨(물론 agg 함수의 연산특성에 따라 다르기는하나, 대부분의 함수가 nan은 배제시키고 계산함)
    # 깜짝 퀴즈
    # 각 row별, nan이 아닌 값이 정확히 top_n개 만큼 인지 확인하는 방법?
    #backtest
    def back_test():
        # 포트폴리오 수익률 데이터
        indicator_df.head()
        # indicator_df.notna.astype(int).replace(0, np.nan)
        #  => nan이 아니면 1, nan이면 nan으로 표기
        asset_on_df = indicator_df.notna().astype(int).replace(0, np.nan)
        asset_on_df.head()

        # 지난 영상 퀴즈 정답1
        yearly_rtn_df.shape
        asset_on_df.shape

        # 지난 영상 퀴즈 정답2
        asset_on_df.notna().sum(axis=1)

        selected_return_df = yearly_rtn_df * asset_on_df
        selected_return_df.head()

        selected_return_df.notna().sum(axis=1)

        a = asset_on_df.iloc[0] # 첫번째 인덱스만 시리즈로 뽑아서 보여줌
        a[a.notna()] # nan이 아닌놈들만 보여줌

        b = yearly_rtn_df.iloc[0]
        b[a[a.notna()].index]

        rtn_series = selected_return_df.mean(axis=1)
        rtn_series.head()

        # 재무제표가 등장한 시점과 수익률이 산정되는 시점, 상장폐지가 되는 시점을 align을 맞추기 어려움. 전처리가 까다로움
        # 새로 수정된 데이터(fin_statement_new.csv)에서는 데이터 2006부터 시작하므로, 2005를 0으로 설정한 점에 주의바랍니다.
        rtn_series.loc[2005] = 0 # 2005라는 index에 0의 값으로 추가됨
        rtn_series = rtn_series.sort_index()
        rtn_series

        # 포트폴리오 누적 수익률 데이터
        # cumprod()
        # 복리효과를 식으로 표현함. 누적수익곡선을 나타내는 시리즈가 됨.
        # cum_rtn_series = (rtn_series + 1).cumprod()
        # 자매품: cumsum()
        cum_rtn_series = (rtn_series + 1).cumprod().dropna()
        cum_rtn_series

        pd.Series([1, 2, 3, 4, 5]).cumsum()

        fig, axes = plt.subplots(nrows=2, figsize=(15, 6), sharex=True)

        axes[0].plot(cum_rtn_series.index, cum_rtn_series, marker='o');
        axes[0].set_title("Cum return(line)");

        axes[1].bar(rtn_series.index, rtn_series);
        axes[1].set_title("Yearly return(bar)");

    # 함수화
    def get_return_series(selected_return_df):
        rtn_series = selected_return_df.mean(axis=1)
        rtn_series.loc[2005] = 0  # 주의: 영상속의 데이터와는 달리, 새로 업로드 된 데이터는 2006부터 존재하므로
        # 2004가 아니라 2005를 0으로 설정한 점에 주의해주세요
        rtn_series = rtn_series.sort_index()

        cum_rtn_series = (rtn_series + 1).cumprod().dropna()
        return rtn_series, cum_rtn_series

    def plot_return(cum_rtn_series, rtn_series):
        fig, axes = plt.subplots(nrows=2, figsize=(15, 6), sharex=True)
        axes[0].plot(cum_rtn_series.index, cum_rtn_series, marker='o');
        axes[1].bar(rtn_series.index, rtn_series);
        axes[0].set_title("Cum return(line)");
        axes[1].set_title("Yearly return(bar)");

    def use_return_func():
        rtn_series, cum_rtn_series = get_return_series(selected_return_df)
        plot_return(cum_rtn_series, rtn_series)

    # 상위 n% 종목 선정
    def quantile():
        quantile_by_year_series = df.groupby(['year'])[indicator].quantile(0.9)
        quantile_by_year_series

        quantilie_indicator_df = df.join(quantile_by_year_series, how="left", on="year", rsuffix="_quantile")
        quantilie_indicator_df.head(2)

        quantilie_indicator_df = quantilie_indicator_df[
            quantilie_indicator_df[indicator] >= quantilie_indicator_df["{}_quantile".format(indicator)]
            ]
        quantilie_indicator_df.head()

        quantilie_indicator_df.groupby('year')['Code'].count()

        indicator_df = quantilie_indicator_df.pivot(index='year', columns="Name", values=indicator)
        asset_on_df = indicator_df.notna().astype(int).replace(0, np.nan)

        selected_return_df = yearly_rtn_df * asset_on_df
        selected_return_df.head()

        rtn_series, cum_rtn_series = get_return_series(selected_return_df)
        plot_return(cum_rtn_series, rtn_series)