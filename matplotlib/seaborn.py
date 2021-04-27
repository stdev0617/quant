import seaborn as sns
import pandas as pd
df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/Small_and_Big.csv", index_col=0, parse_dates=["date"])

def seabornBasic():
    median_df = df.groupby(['date']).agg({'시가총액 (보통)(평균)(원)': 'median'})
    median_df.columns = ["median_시가총액"]
    median_df.head()
    df = df.join(median_df, on="date")
    df.loc[df['시가총액 (보통)(평균)(원)'] < df['median_시가총액'], "size"] = "small"
    df.loc[df['시가총액 (보통)(평균)(원)'] >= df['median_시가총액'], "size"] = "big"
    df.head()

    # count plot
    # matplotlib version
    df['size'].value_counts()
    df['size'].value_counts().plot(kind='bar');
    df['size'].hist()

    # seaborn version
    sns.countplot(x="size", data=df)

    # 수익률 bar plot
    df.shape
    # 데이터 사이즈 줄이기
    df = df[df['date'] >= "2017-01-01"]
    df.shape
    df.head()

    # matplotlib version
    df.groupby(['date'])['수익률(%)'].mean()
    df.groupby(['date'])['수익률(%)'].mean().plot(kind='bar', figsize=(18, 3))

    # 날짜 x tick label을 조금더 심플하게 나타나도록 만들기: DateTime object -> 문자열 object로 변환
    df['date'] = df['date'].dt.strftime("%Y-%m-%d")  # %Y, %m 등과 같은 표현에 대해서 조금더 자세하게 알고 싶으신 분은 구글에 python datetime format으로 검색해보세요!
    # datetime
    # strftime
    # strptime
    df.groupby(['date'])['수익률(%)'].mean().plot(kind='bar', figsize=(18, 3))

    # seaborn version
    sns.barplot(data=df, x="date", y="수익률(%)")
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18, 3))
    ax = sns.barplot(data=df, x="date", y="수익률(%)", ax=ax);

    # x tick label을 45도 돌리기
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18, 3))
    ax = sns.barplot(data=df, x="date", y="수익률(%)", ax=ax);

    current_x_tick_label = ax.get_xticklabels()
    ax.set_xticklabels(current_x_tick_label, rotation=45);

    # hue 넣기
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18, 3))
    sns.barplot(data=df, x="date", y="수익률(%)", ax=ax, hue="size")

    current_x_tick_label = ax.get_xticklabels()
    ax.set_xticklabels(current_x_tick_label, rotation=45);

def multiDimensionGraph():
    df.head(2)
    sns.relplot(
        x="PBR(IFRS-연결)",
        y="수익률(%)",
        col="size",
        hue="베타 (M,5Yr)",
        data=df,

        palette="coolwarm",
    )

    with sns.plotting_context("notebook", font_scale=1.2):
        sns.relplot(
            x="PBR(IFRS-연결)",
            y="수익률(%)",
            col="size",
            hue="베타 (M,5Yr)",
            palette="coolwarm",
            data=df
        )

    with sns.plotting_context("notebook", font_scale=1.2):
        sns.relplot(
            x="PBR(IFRS-연결)",
            y="수익률(%)",
            size="size",  # `col` 대신 `size`사용
            hue="베타 (M,5Yr)",
            palette="coolwarm",
            data=df
        )

def seabornExample():
    df_list = []
    for i in range(2015, 2018):
        df_list.append(
            pd.read_csv("my_data/naver_finance/{}_12.csv".format(i))
        )
    df = pd.concat(df_list)
    df.head()
    df = df.dropna()
    df['rtn'] = df['price2'] / df['price'] - 1

    #
    # outlier(이상치) 제거하기
    #
    for col in df.columns:
        if col not in ['ticker', 'price2', 'price', 'rtn']:
            mu = df[col].mean()
            std = df[col].std()

            cond1 = mu - 2 * std <= df[col]
            cond2 = df[col] <= mu + 2 * std

            df = df[cond1 & cond2]

    # with sns.plotting_context("notebook", font_scale=1.2):
    sns.relplot(
        x="순이익률(%)",
        y="rtn",
        hue="ROA(%)",
        palette="coolwarm",
        data=df
    )

    # with sns.plotting_context("notebook", font_scale=1.2):
    sns.relplot(
        x="PSR(배)",
        y="rtn",
        hue="당기순이익(억원)",
        palette="coolwarm",
        data=df
    )

    # https://seaborn.pydata.org/examples/index.html 참고
