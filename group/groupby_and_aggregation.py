import matplotlib
import pandas as pd
import numpy as np
import FinanceDataReader as fdr

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Split(그룹으로 split) - Apply(연산적용) - Combine(다시 합침)
df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/naver_finance/2016_12.csv")
print(df.shape)

df = df.dropna()
print(df.shape)

g_df = df.copy()
print(g_df.head())

g_df['rtn'] = df['price2'] / df['price'] - 1

g_df.loc[:, 'PER_score'] = pd.qcut(g_df['PER(배)'], 10, labels=range(1, 11))
g_df.loc[:, 'PBR_score'] = pd.qcut(g_df['PBR(배)'], 10, labels=range(1, 11))

g_df.set_index('ticker', inplace=True)


# groupby() - 실제로 grouping까지는 하지 않고, grouping이 가능한지 validation만 진행(preparation)
# aggregation - 2가지 요소로 구성
# aggregating columns
# aggregating funtions - e.g, sum, min, max, mean, count, variance, std etc
# 결국 3가지 요소만 충족시키면 됨!
# Grouping columns(categorial data type)
# Aggregating columns
# Aggregating functions - 강의에서는 배우지 않지만, transform(), apply(), filter() 등도 있음. 알아두면 좋음

def groupby():
    # g_df.groupby('PER_score')
    g_df_obj = g_df.groupby(["PBR_score", "PER_score"])
    print(type(g_df_obj)) # 결과를 보면 결과가 <pandas.core.groupby.generic.DataFrameGroupBy object at 0x119dea928> 이렇게 나옴.
                          # validation을 진행했기때문
    g_df_obj.ngroups # 결과는 96
    print(g_df['PBR_score']) # 이렇게하면 각 회사가 몇분위에 속하는지가 나옴
    g_df['PBR_score'].nunique()
    g_df['PER_score'].nunique()
    print(g_df_obj.size()) # PBR 분위별로 PER 분위가 각각 몇개있는지 나옴
    print(g_df_obj.size().loc[1]) # PBR의 1분위 안에있는 PER만 나옴
    print(g_df_obj.size().loc[(1,1)]) # PBR의 1분위 안에있는 PER 1분위값만 나옴
    print(g_df_obj.size().to_frame()) # frame형태로 보여줌

    type(g_df_obj.groups) # dictionary임.
    print(g_df_obj.groups.keys())

    # print whole group names(labels)
    list(g_df_obj.groups.keys())[:10]
    # Retrieve specific group
    g_df_obj.get_group((1, 1)).head(2) # 해당 그룹의 데이터 프레임이 나오게됨

    # For loop을 이용해서 grouping된 object 확인해보기(많이는 안쓰임)
    for name, group in g_df_obj:
        print(name)
        group.head(2)
        break

    # 주의: 여기서 head()는 최상위 2개를 가지고 오는게 아니라
    # 각 그룹별 최상위 2개를 무작위로 섞어서 하나로 합친 DataFrame을 리턴한다
    g_df.groupby('PER_score').head(2)

# aggregation
# min, max, mean, median, sum, var, size, nunique, idxmax

def aggregation():
    g_df_obj = g_df.groupby(["PBR_score", "PER_score"])
    pbr_rtn_df = g_df.groupby("PBR_score").agg({'rtn': 'mean'}) # 아래 다른것들보다 이 형태를 가장 추천함. 거의 모든 케이스에 대해 커버가 가능하기때문
    per_rtn_df = g_df.groupby("PER_score").agg({'rtn': 'mean'})
    g_df.head()

    g_df.groupby("PBR_score").agg(
        {
            "rtn": "mean", # np.mean
        }
     )

    g_df.groupby("PER_score")['rtn'].agg("mean")
    g_df.groupby("PER_score")[['rtn']].agg("mean")
    g_df.groupby("PER_score")[['rtn', 'PBR(배)']].agg("mean")

    g_df.groupby("PER_score")[['rtn', 'PBR(배)']].agg(["mean", "std"]) # mean, std가 각각 구해짐


    # <같은결과>
    g_df.groupby("PER_score")['rtn'].agg('mean').head()
    g_df.groupby("PER_score")['rtn'].agg(np.mean).head()
    g_df.groupby("PER_score")['rtn'].mean().head()
    g_df.groupby("PER_score")[['rtn']].mean().head()

    np.sqrt([1, 2, 3, 4])
    # g_df.groupby("PER_score")['rtn'].agg(np.sqrt) # error

    pbr_rtn_df.plot(kind='bar')
    per_rtn_df.plot(kind='bar')

def example_for_groupby():
    g_df1 = g_df.groupby(["PBR_score", "PER_score"])\
                .agg({
                        'rtn': ['mean', 'std', 'min', 'max'],
                        'ROE(%)': [np.mean, 'size', 'nunique', 'idxmax']
                })
    g_df1.head()

    #다른 방법
    g_df.groupby(["PBR_score", "PER_score"])['rtn', 'ROE(%)'].agg(['sum', 'mean']).tail(10)
    a = g_df.groupby(["PBR_score", "PER_score"])['rtn', 'ROE(%)'].agg(['sum', 'mean'])

    # Multi-index라고 해서 쫄 것 없음!
    a.loc[1]
    a.loc[(1, 3)]
    a.loc[[(1, 3)]]
    # a.loc[[1, 3]]

    # 주의) nan은 groupby시 자동으로 filter out 되기 때문에, 미리 전처리 다 하는게 좋음
    df = pd.DataFrame({
        'a': ['소형주', np.nan, '대형주', '대형주'],
        'b': [np.nan, 2, 3, np.nan],
    })

    print(df)
    print(df.groupby(['a'])['b'].mean()) # nan값을 제외하고 평균을 냄. 그래서 대형주는 평균값이 3000이 나오고, 소형주는 nan이 나옴

    # as_index = False: group col들이 index가 아니라 하나의 col이 됨(aggregate하고 reset_index()를 취한 것)
    a = g_df.groupby(["PER_score"]).agg({'rtn': ['mean', 'std']}).head(2)
    b = g_df.groupby(["PER_score"], as_index=False).agg({'rtn': ['mean', 'std']}).head(2)

    print(a)
    print(b)

    print(a.index)
    print(a.columns)

    print(b.index)
    print(b.columns)

    print(a['rtn'])
    print(a[('rtn', 'mean')].head())

    # Squash the Multi-index columns
    g_df1.head()

    level0 = g_df1.columns.get_level_values(0)
    level1 = g_df1.columns.get_level_values(1)

    print(level0)
    print(level1)

    g_df1.columns = level0 + '_' + level1
    print(g_df1.head(2))

    g_df1 = g_df1.reset_index() # df에 인덱스를 다 채워서 보여줌
    print(g_df1.head())

def example2_for_groupby():
    a_df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/Small_and_Big.csv", index_col=[0])
    a_df.head()

    a_df.tail()

    median_df = a_df.groupby(['date']).agg({'시가총액 (보통)(평균)(원)': 'median'})
    median_df.columns = ['시가총액_median']
    print(median_df.head())