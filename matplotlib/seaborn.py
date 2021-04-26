import seaborn as sns
import pandas as pd
df = pd.read_csv("C:/Users/owner/Downloads/inflearn_pandas_part1_material/my_data/Small_and_Big.csv", index_col=0, parse_dates=["date"])
print(df.head())

median_df = df.groupby(['date']).agg()