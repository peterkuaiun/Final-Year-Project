import pandas as pd
x = []
y = []

df = pd.read_table("simple_graph", skiprows=1 ,sep=" ", header=None)
df_x = df.iloc[0:100, [1]] 
df_y = df.iloc[0:100, [2]] 