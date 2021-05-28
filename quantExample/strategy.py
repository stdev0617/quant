import numpy as np
import pandas as pd
import warnings

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

warnings.filterwarnings('ignore')

pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('max_columns', None)

# 영상에서는 fin_statement_2005_2017.csv이지만(데이터 문제가 있는 파일),
# 해당 데이터에서 문제를 발견하여, fin_statement_new.csv라는 데이터(2006 ~ )로 대체되었습니다
df = pd.read_csv("my_data/fin_statement_new.csv")
df.head()

# 5.1 quantile+top10
# Filter + Selector 구조
# - Filter
#   - e.g, 부채비율 0.5이상
#   - 최종 포트폴리오 종목 갯수 선정에 직접적으로 영향X
# - Selector
#   - 최종적으로 xx개의 종목이 선택의 기준이 되는 indicator
#   - e.g. PBR이 0.2 이상이면서, PBR이 가장 낮은 주식순으로 2~30개 매수

# 5.2 [Chapter 6] 투자전략22. 소형주+저PBR 전략(200p)
# - Filter
#   - 소형주(시가총액 하위 20%)
# - Select
#   - (PBR 0.2 이상) // select의 기준이 되기도 하므로
#   - PBR이 가장 낮은 주식순으로 2~30개 매수

# 거래세, 수수료는 고려가 안됨
# 상장폐지는 고려 안했음
def get_return_series(selected_return_df):
    rtn_series = selected_return_df.mean(axis=1)
    rtn_series.loc[2005] = 0     # 주의: 영상속의 데이터와는 달리, 새로 업로드 된 데이터는 2006부터 존재하므로
                                 # 2004가 아니라 2005를 0으로 설정한 점에 주의해주세요
    rtn_series = rtn_series.sort_index()

    cum_rtn_series = (rtn_series + 1).cumprod().dropna()
    return rtn_series, cum_rtn_series

def makeSmallStockAndLowPBRStrategy():
    market_cap_quantile_series = df.groupby("year")['시가총액'].quantile(.2)

    filtered_df = df.join(market_cap_quantile_series, on="year", how="left", rsuffix="20%_quantile")
    filtered_df = filtered_df[filtered_df['시가총액'] <= filtered_df['시가총액20%_quantile']]
    print(filtered_df.head())

    filtered_df = filtered_df[filtered_df['PBR'] >= 0.2]

    smallest_pbr_series = filtered_df.groupby("year")['PBR'].nsmallest(15)
    print(smallest_pbr_series)

    selected_index = smallest_pbr_series.index.get_level_values(1)

    selector_df = filtered_df.loc[selected_index].pivot(
        index='year', columns="Name", values="PBR"
    )
    selector_df.head()

    # nan을 0으로 치환 후 계산
    asset_on_df = selector_df.notna().astype(int).replace(0, np.nan)
    selected_return_df = yearly_rtn_df * asset_on_df

    rtn_series, cum_rtn_series = get_return_series(selected_return_df)
    plot_return(cum_rtn_series, rtn_series)

# Filter
#  - ROA 5% 이상
#  - 부채비율 50% 이하
# Select
#  - (PBR 0.2 이상)
#  - PBR 낮은기업 20~30개 매수
def lastPresentUpgrade():
    #
    # Filter
    #

    # ROA >= 0.05
    filtered_df = df[df['ROA'] >= 0.05]

    # 부채비율 <= 0.5
    filtered_df['부채비율'] = filtered_df['비유동부채'] / filtered_df['자산총계']
    filtered_df = filtered_df[filtered_df['부채비율'] <= 0.5]

    #
    # Selector(위의 투자전략22 것 그대로)
    #
    filtered_df = filtered_df[filtered_df['PBR'] >= 0.2]

    smallest_pbr_series = filtered_df.groupby("year")['PBR'].nsmallest(15)
    selected_index = smallest_pbr_series.index.get_level_values(1)

    selector_df = filtered_df.loc[selected_index].pivot(
        index='year', columns="Name", values="PBR"
    )

    asset_on_df = selector_df.notna().astype(int).replace(0, np.nan)
    selected_return_df = yearly_rtn_df * asset_on_df

    rtn_series, cum_rtn_series = get_return_series(selected_return_df)
    plot_return(cum_rtn_series, rtn_series)

# 슈퍼가치전략
# * Filter
#  - 시가총액 하위 20%
# * Selector
#  - PBR, PCR, PER, PSR 순위를 매김
#  - 각 순위를 sum을 해서 통합순위를 구함
#  - 통합순위가 가장 높은 종목 50개 매수
def superValueStrategy():
    #
    # Filter
    #
    market_cap_quantile_series = df.groupby("year")['시가총액'].quantile(.2)
    filtered_df = df.join(market_cap_quantile_series, on="year", how="left", rsuffix="20%_quantile")
    filtered_df = filtered_df[filtered_df['시가총액'] <= filtered_df['시가총액20%_quantile']]

    pd.Series([100, 1, 1, 3]).rank(method="max")
    pd.Series([100, 1, 1, 3]).rank(method="min")

    pbr_rank_series = filtered_df.groupby("year")['PBR'].rank(method="max")
    per_rank_series = filtered_df.groupby("year")['PER'].rank(method="max")
    psr_rank_series = filtered_df.groupby("year")['PSR'].rank(method="max")

    psr_rank_series.head()

    psr_rank_series.sort_values().dropna().head()

    filtered_df = filtered_df.join(pbr_rank_series, how="left", rsuffix="_rank")
    filtered_df = filtered_df.join(per_rank_series, how="left", rsuffix="_rank")
    filtered_df = filtered_df.join(psr_rank_series, how="left", rsuffix="_rank")

    filtered_df['PBR_rank'].isna().sum()

    # 어떻게 각 rank column의 nan을 메꿔야할까?
    filtered_df.filter(like="rank").columns

    #
    # 주의: 종목을 선택하는 로직ㅇ[ 따라, '가장 작은 rank'로 부여하는게 타당할 수도 있고, '가장 큰 rank'로 부여하는 것이 타당할 수도 있습니다.
    # 예를들어, PER이 작을수록 종목 선정에 우선 순위가 있도록 할 예정이고, PER이 작을수록 rank값이 작도록 설정했다면,
    # PER이 nan인 종목들은 PER rank가 가장 큰 값(혹은 그 값보다 +1인 값)으로 메꿔져야 penalty를 받을 수 있습니다.
    #

    # 1. 0으로 메꾸는 법
    filtered_df.loc[:, filtered_df.filter(like="rank").columns] = filtered_df.filter(like="rank").fillna(0)

    # 2. 각 rank별 max 값 (혹은 그것보다 1 큰 값)으로 메꾸는 법
    # filtered_df['PBR_rank'] = filtered_df['PBR_rank'].fillna(filtered_df['PBR_rank'].max() + 1)
    # filtered_df['PER_rank'] = filtered_df['PER_rank'].fillna(filtered_df['PER_rank'].max() + 1)
    # filtered_df['PSR_rank'] = filtered_df['PSR_rank'].fillna(filtered_df['PSR_rank'].max() + 1)

    filtered_df['rank_sum'] = filtered_df.filter(like="_rank").sum(axis=1)

    #
    # Selector
    #
    max_rank_series = filtered_df.groupby("year")['rank_sum'].nlargest(15)
    selected_index = max_rank_series.index.get_level_values(1)

    selector_df = filtered_df.loc[selected_index].pivot(
        index='year', columns="Name", values="rank_sum"
    )

    asset_on_df = selector_df.notna().astype(int).replace(0, np.nan)
    selected_return_df = yearly_rtn_df * asset_on_df

    rtn_series, cum_rtn_series = get_return_series(selected_return_df)
    plot_return(cum_rtn_series, rtn_series)


# 재무제표 기반 실전 프로젝트의 한계¶
# 1. (중요)Look ahead bias & Survivalship bias
#  - 특정 년도에 상장이 폐지가 되었다면 -> 바로 이전 년도에서 종목선정에 고려가 안됨
#  - 즉, 이미 상장 폐지 정보를 미래 시점에서 확인하고, 해당 년도의 수익률을 nan으로 미리 메꾸어 버림
# 2. Data availability(time alignment)
#  - 각 투자지표의 값들이 공시 되는 시기
#     - 년도별, 분기별
#  - 정확한 상장폐지 날짜?
# 3. Data acquisition
#  - 고정된 과거데이터로만 테스트 하면 안됨 -> 계속 새로운 데이터에 대한 갱신 필요
#  - 크롤링, 증권사 API, 유료 데이터 벤더 등
# 4. Data의 무결성
#  - 아무리 증권사 API나 유로 벤더를 통해서 받아온 데이터라도, 문제가 있는 경우가 많음
#  - 예를 들어, 일봉 OHLC -> C가 H보다 더 큰 경우 / 배당락, 주식분할 등의 이벤트가 제대로 반영이 안된 경우 등
#  - 데이터의 결함, nunique==1, 비이상적인 값 등에 대한 EDA 필요
# 5. 데이터가 년도별로만 존재하기 때문에, 1년에 한번 수익률이 찍혀서 변동성, MDD를 제대로 파악하기 어려움
# 6. 거래세, 수수료 반영 X
#  - 정확한 asset turnover 고려가 안됨
# 7. 기타 위 실전예제에서의 한계
#  - 데이터의 cleaning, validation 필요
#  - Missing value에 대한 전처리 필요
#  - 주어진 데이터 존재하지 않는 지표(column)은 다른 지표로 대체한 점

# 혼자 진행해보면 좋을 것들
#  - transform(), apply() 함수 등을 구글링해서 독학해보기
#  - OOP 방식으로 구현해보기(확장성 있는 코드화)
def etc():
    filter_list = [
        ColumnIndicator("부채비율", 0.5, lower_than=False),
        ColumnIndicator("ROE", 0.5, lower_than=True),
    ]
    selector = Selector("PBR", 20, lowest=True)

    backtest = Backtest(filter_list, selector, yearly_rtn_df)
    backtest.run()

    # 거래비용 주기
    for_positive_df = (yearly_rtn_df > 0).astype(int) * 0.99
    for_negative_df = (yearly_rtn_df < 0).astype(int) * 1.01

    extra_fee_considered_weight_df = for_positive_df + for_negative_df
    yearly_rtn_df = yearly_rtn_df * extra_fee_considered_weight_df

    # weight
    #
    #  - 지금까지는 종목 선택 후, 다 동일가중 투자(mean()만으로 평균수익률을 구할 수 있었음)
    #  - e.g. ROA의 비중만큼 넣기
    #     - Top n개의 종목을 산출 후, 각각의 값을 1,0(nan)으로 변환하기 전에, selector_df를 sum(axis=1)로 나눠주기 등
    #  - 분기별 데이터 & 리벨런싱