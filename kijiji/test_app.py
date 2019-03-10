
import pandas as pd

df = pd.read_json('test/unclean_data.json', orient='records')

print(df)
