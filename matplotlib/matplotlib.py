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
