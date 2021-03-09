import numpy as np
import pandas as pd

def test_series():
    obj = pd.Series()
    a = pd.Series([1, 2, 3, 4])
    type(a)

    # series 생성 첫번째 방법
    s2 = pd.Series(
        [1, 2, 3, 4],
        index=['a', 'b', 'c', 'd']
    )
    print(s2.head()) # head의 앞의 값들을 보여줌. default 5개

    s2 = pd.Series({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
    print(s2.head())

def test_nan():
    s = pd.Series([10, 0, 1, 1, 2, 3, 4, 5, 6, np.nan])
    print(s)

    print(len(s)) # 10 Series의 총 길이
    print(s.count()) # 9 즉, nan 제외
    print(s.unique()) # 중복값 제외해서 보여줌. nan도 포함해서 보여줌.
    print(s.value_counts()) #series에 대해서 operation을 해서 series를 결과로 돌려줌. 다른건 다 list 형태로 보여줌. nan은 포함되지 않음.
    
def test_series_operation():
    s3 = pd.Series([1,2,3,4],index=['a','b','c','d'])
    s4 = pd.Series([4,3,2,1],index=['d','c','b','a'])
    print(s3)
    print(s4)
    print(s3+s4) # index가 같은 것끼리 연산함
