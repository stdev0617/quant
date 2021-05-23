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