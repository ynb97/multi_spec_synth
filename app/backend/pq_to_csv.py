import pandas as pd
df = pd.read_parquet('data-00001-of-00002.parquet')
df.to_csv('filename.csv')