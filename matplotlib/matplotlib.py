import matplotlib.pyplot as plt
import numpy as np
import FinanceDataReader as fdr;

# matplotlib 2가지 구성요소
# Figure: 틀 / Axes: Figure 바로 아래에, 실제 그래프가 그려질 공간. 이 안에 각종 plotting components가 존재

samsung_df = fdr.DataReader('005930', '2017-01-01', '2017-12-31')
print(samsung_df.head())

# 2.1 Stateful
# Matplotlib이 암묵적으로 현재 상태를 들고있음
# - 내부적으로 현재 타겟이 되는 figure, ax 등을 설정하고, operation이 발생하면 내부에서 해당 figure, ax에 적용함
# 사용은 비추
# - matplotlib이 암묵적, 내부적으로 변화를 진행하고, 적용하기 때문에, 직관적이지 못함
# - 다수의 plot을 한 번에 그리기 어려움
# - 그냥 간단히 테스트 해볼 때 정보에만 사용

def stateful():
    x = [1, 2, 3]
    y = [4, 5, 6]
    plt.plot(x, y);
    plt.show();

    x = [-1, 5, 7]
    y = [10, 2, 5]

    plt.figure(figsize=(15,3));
    plt.plot(x, y);
    plt.xlim(0, 10);
    plt.ylim(-3, 8);
    plt.xlabel('x_Axis');
    plt.ylabel('y_Axis');
    plt.title('Line Plot');
    plt.suptitle('Figure Title', size=10, y=1.03);

    # 아래는 index (timeseries), column 매핑을 통해 값을 출력하는 예제
    plt.plot(samsung_df, samsung_df['Close']);

# Stateless(or object-oriented)
# Matplotlib의 component를 하나의 object로 받아서, 함수 실행 및 property 설정/변경
#   - figure, ax(es)를 먼저 생성한다음, 하나하나 더하고, 적용하는 식
# 적용과정이 명시적으로 코드로 드러나기 때문에 조금 더 직관적임
# plot을 객체로 만든다고 생각하면 편할듯
def stateless():
    fig, ax = plt.subplots(figsize=(15, 3))
    ax.plot(x, y);
    ax.set_xlim(0, 10);
    ax.set_ylim(-3, 8);
    ax.set_xlabel('X axis');
    ax.set_ylabel('Y axis');
    ax.set_title('Line Plot');
    fig.suptitle('Figure Title', size=10, y=1.03);

    fig, ax = plt.subplots(figsize=(15, 3))
    ax.plot(samsung_df.index, samsung_df['Close'])

# Matplotlib components에 대해 조금 더 깊게 들여다보기
def matplotlibComponents():

    # figure, axes
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10)) # 차트 4개를 10*10 fig에 그림. 리턴은 전체 하나, 각각의 차트 하나씩
    print(axes[0][0]) # 배열처럼 차트를 가져올 수 있음.
                      # nrows or ncols가 1보다 크면, ax의 type은 AxesSubplot가 아니라 numpy array of AxesSubplot임

    # Children of ax(es)
    axes[0][0].get_children() # spines: axes를 둘러싸고 있는 border
                              # axis: x,y축. ticks, labels 등을 가지고 있음
    # axis는 객체이기 때문에 값을 가져올 때, get 함수로 값을 가져올 수 있다.
    ax.xaxis == ax.get_xaxis() # true
    ax = axes[0][0]

    # example
    data = fdr.DataReader("005930", start="2019-01-01", end="2020-01-01")
    close_series = data['Close']
    volume_series = data['Volume']

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14,10), sharex=True) # shareX는 차트가 x축을 위아래 같은 값을 갖는것을 뜻함

    ax1 = axes[0]
    ax2 = axes[1]

    ax1.plot(close_series.index, close_series, linewidth=2, linestyle='--', label="Close")
    _ = ax1.set_title('Samsung price', fontsize=15, family='Arial');
    _ = ax1.set_ylabel('price', fontsize=15, family='Arial');
    _ = ax1.set_xlabel('date', fontsize=15, family='Arial');
    ax1.legend(loc="upper left");

    ax2.plot(close_series.index, volume_series, label="Volume");
    _ = ax2.set_title('Samsung volume', fontsize=15, family='Arial');
    _ = ax2.set_ylabel('volume', fontsize=15, family='Arial');
    _ = ax2.set_xlabel('date', fontsize=15, family='Arial');
    ax2.legend(loc="upper left");

    fig.suptitle("<Samsung>", fontsize=15, family='Verdana');

    fig, ax = plt.subplots()
    ax.plot([5, 6, 7, 8]) # y축 값이 5~8까지 나옴

    # set_ticks vs set_ticklables
    # set_tics(): setting range of ticks (xaxis에 매달려 있는 'l'의 range)
    # set_ticklables(): tick labels itself
    a = pd.Series([1, 2, 3], index=pd.period_range("2000-10-01", "2000-12-31", freq="1M"))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 3))

    # pandas로 바로 그리면 안됨.(e.g a.plot())
    ax.plot([np.nan] + a.values.tolist() + [np.nan], marker='o')

    # set_ticks와 set_ticklabels에 넣는 인자의 길이는 같아야함!
    _ = ax.xaxis.set_ticks(np.arange(5));
    _ = ax.xaxis.set_ticklabels(pd.period_range("2000-09-01", "2001-01-31", freq="1M"), rotation=45);
    print(ax.figure)






