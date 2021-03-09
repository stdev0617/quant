import numpy as np
import pandas as pd

# DataFrame
# 다수의 Series를 하나의 변수로 관리할 수 있도록 만든 자료형
# Series의 dict 형태라고 보면 됨
# usage: {'col1': series1, 'col2': series2}
# 각 Series는 DataFrame의 column을 이룸
# 당연히 DataFrame을 이루는 Series간의 index는 서로 다 같음! => 동일 index 사용

# DataFrame을 만드는 다양한 방법들
def test_dataframe():
    s1 = np.arange(1, 6, 1) # 1~5까지 1씩 증가시킨 array
    s2 = np.arange(6, 11, 1) # 6~10까지 1씩 증가시킨 array
    print(pd.DataFrame({'c1': s1, 'c2': s2})) # c1,c2가 column attr, index가 row attr인 테이블 형태로 결과를 출력한다. 이걸 제일 많이 씀.
    print(pd.DataFrame([[10,11],[10,12]])) # 이 행렬 형태로 결과를 출력함
    print(pd.DataFrame(np.array([[10,11],[20,21]]))) # 이 행렬 형태로 결과를 출력함
    print(pd.DataFrame([pd.Series(np.arange(10,15)),pd.Series(np.arange(15,20))])) # 2 * 5 행렬이 만들어짐. but 잘 안씀
    print(pd.DataFrame([np.arange(10,15),np.arange(15,20)])) # 2 * 5 행렬이 만들어짐. but 잘 안씀

    print(pd.DataFrame({'c1': [0], 'c2': [1]})) # 참고) 한 줄짜리 만들 때도 value들은 list type으로 설정해줘야한다

def make_with_colume_and_index_names():
    print(pd.DataFrame(np.array([[10,11],[20,21]]),columns=['a','b'],index=['r1','r2']))

def test_index_names():
    s1 = pd.Series(np.arange(1, 6, 1), index=['a', 'b', 'c', 'd', 'e'])
    s2 = pd.Series(np.arange(6, 11, 1), index=['b', 'c', 'd', 'f', 'g'])
    print(pd.DataFrame({'c1': s1, 'c2': s2})) # 인덱스에 값이 없으면 nan으로 출력

def add_column_to_dataframe():
    s1 = pd.Series(np.arange(1, 6, 1), index=['a', 'b', 'c', 'd', 'e'])
    s2 = pd.Series(np.arange(6, 11, 1), index=['b', 'c', 'd', 'f', 'g'])
    s3 = pd.Series(np.arange(12, 15), index=[1, 2, 10])
    df = pd.DataFrame({'c1':s1, 'c2': s2, 'c3': s3})
    df['c4'] = pd.Series([1,2,3,4], index=[0,1,2,10]) # c4라는 column이 추가된다.
    print(df)