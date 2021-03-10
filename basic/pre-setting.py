import numpy as np
import pandas as pd
# 하나의 cell에서 multiple output 출력을 가능하게 하는 코드
# jupyter용인듯. 이거안쓰면 여러 값을 cout 출력해도 마지막 코드 하나만 나타나게됨.
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Pandas Dataframe의 사이즈가 큰 경우, 어떻게 화면에 출력을 할지 세팅하는 코드
pd.set_option('display.float_format', lambda x: '%.3f' % x)
# 출력값에서 column이 많은 경우 ...으로 줄어들지 않고, 모든 컬럼을 보여주도록 하는 코드
pd.set_option('max_columns', None)