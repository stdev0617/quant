import numpy as np

def test_numpy():
    a = np.array([1,2,3])
    print("a: ", a) # [1 2 3]
    print("type(a): ", type(a)) #<class 'numpy.ndarray'>
    print("a[0]: ", a[0]) # 1

def test_universal_func():
    a = [1, 2, 3]
    b = [4, 5, 6]

    new_list = []
    for e1, e2 in zip(a, b):
        new_list.append(e1 + e2)
    print(new_list) # [5, 7, 9]
    print(a+b) # [1, 2, 3, 4, 5, 6]

def test_universal_func2():
    a = np.array([1,2,3])
    b = np.array([4,5,6])
    print(a) # [1 2 3]

    print(a+b) # [5 7 9] 그냥 List를 더하는 것과 np.array를 더하는 것은 결과가 다름. List는 List의 합이고, np.array는 각 백터의 합임

    print(np.sum(a)) # 6
    print(np.abs(a)) # [1 2 3]
    print(np.log(a)) # [0.         0.69314718 1.09861229]
    print(np.exp(a)) # [ 2.71828183  7.3890561  20.08553692]
    print(np.isnan(a)) # [False False False]

def test_2d_array():
    a = np.array([[1,2], [3,4]])
    print(a[0][1]) # 2