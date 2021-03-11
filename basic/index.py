import pandas as pd
import numpy as np

def reindexing():
    s = pd.Series([1,2,3,4,5])
    print(s)
    # index 변경
    s.index=['a','b','c','d','e']
    print(s.head())
    s1 = pd.Series(np.arange(1, 6, 1), index=['a', 'b', 'c', 'd', 'e'])
    s2 = pd.Series(np.arange(6, 11, 1), index=['b', 'c', 'd', 'f', 'g'])
    s3 = pd.Series(np.arange(12, 15), index=[1, 2, 10])
    df = pd.DataFrame({'c1':s1, 'c2': s2, 'c3': s3})
    df['c4'] = pd.Series([1,2,3,4], index=[0,1,2,10]) # c4라는 column이 추가된다.
    df['c5'] = pd.Series([1,2,3,4,5,6], index=[0,1,2,3,4,10])
    print(df)
    df.set_index("c5") # 테이블의 index가 기본 null이지만, 이걸통해 index를 줄 수 있다.

    s = pd.Series(np.arange(1,6,1), index=['a', 'b', 'c', 'd', 'e'])
    # 시리즈 중에서 원하는 인덱스와 값을 가져와서 하나로 만들 수 있다.
    s2 = s.reindex(['a','c','e','g'])
    print(s2)

    # copied
    s2['a'] = 0
    print(s2)

    # 이렇게 하면 안됨
    s1 = pd.Series([0,1,2], index=[0,1,2])
    s2 = pd.Series([3,4,5], index=['0','1','2'])
    print(s1+s2) # 모두 nan 값. nan+x = nan

    #s2 = s2.reindex(s1.index) # 모두 nan... 매핑되는게 없으니..

    # 해결방법1
    s2.index = s2.index.astype(int)
    print(s1+s2) # 결과 정상

    # 해결방법2
    s1.index = ['a','b','c']
    s2.index = ['a','b','c']
    print(s1 + s2)

    s2 = s.copy()
    print(s2)

    s2.reindex(['a','f'], fill_value=0) # nan으로 0으로 채워줌

    s3 = pd.Series(['red','green','blue'], index=[0,3,5])
    s3.reindex(np.arange(0,7))
    # ffill은 forward fill 로써, 이전에 있는 값으로 매꾸는 것
    s3.reindex(np.arange(0,7), method='ffill')

